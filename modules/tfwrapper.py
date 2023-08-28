import os
import sys
from pathlib import Path
import click
import modules.gitlibs as gitlibs
import modules.helpers as helpers
import tempfile
import shutil
import json

# Create Tempdir and Module Cache Directories
annotations = dict()
start_dir = Path.cwd()
temp_dir = tempfile.TemporaryDirectory(dir=tempfile.gettempdir())
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
MODULE_DIR = str(Path(Path.home(), ".terravision", "module_cache"))


def tf_initplan(source: tuple, varfile: list):
    for sourceloc in source:
        if os.path.isdir(sourceloc):
            os.chdir(sourceloc)
        else:
            githubURL, subfolder, git_tag = gitlibs.get_clone_url(sourceloc)
            codepath = gitlibs.clone_files(sourceloc, temp_dir.name)
            shutil.copy("override.tf", codepath)
            os.chdir(codepath)
        returncode = os.system(f"terraform init")
        if returncode > 0:
            click.echo("ERROR running terraform init command")
            exit()
        vfile = varfile[0]
        click.echo("\nRunning terraform plan..")
        returncode = os.system(f"terraform plan -var-file {vfile} -out tfplan.bin")
        click.echo("Analysing plan..")
        if (
            os.path.exists("tfplan.bin")
            and os.system(f"terraform show -json tfplan.bin > tfplan.json") == 0
        ):
            f = open("tfplan.json")
            plandata = json.load(f)
            returncode = os.system(f"terraform graph > tfgraph.dot")
            if os.path.exists("tfgraph.dot"):
                returncode = os.system(f"dot -Txdot_json -o tfgraph.json tfgraph.dot")
                f = open("tfgraph.json")
                graphdata = json.load(f)
            else:
                click.echo("ERROR running terraform graph")
                exit()
        else:
            click.echo("ERROR running terraform plan")
            exit()
    os.chdir(start_dir)
    return make_tf_data(plandata, graphdata)


def make_tf_data(plandata: dict, graphdata: dict):
    tfdata = dict()
    tfdata["tf_resources_created"] = plandata["resource_changes"]
    tfdata["tfgraph"] = graphdata
    return tfdata


def tf_makegraph(tfdata: dict) :
    tfdata["graphdict"] = dict()
    tfdata["meta_data"] = dict()
    tfdata["node_list"] = list()
    tfdata["hidden"] = dict()
    tfdata["annotations"] = dict()
    gvid_table = list()
    # Make an initial dict with resources created and empty connections
    for object in tfdata["tf_resources_created"] :
        node = object["address"].replace("[","-")
        node = node.replace("]","")
        no_module_name = helpers.get_no_module_name(node)
        tfdata["graphdict"][no_module_name] = list()
        tfdata["node_list"].append(no_module_name)
        # add metadata
        details = object["change"]["after"]
        details.update(object["change"]["after_unknown"])
        details.update(object["change"]["after_sensitive"])
        tfdata["meta_data"][no_module_name] = details
    # Make a lookup table of gvids mapping resources to ids
    for item in tfdata["tfgraph"]["objects"]:
        gvid = item["_gvid"]
        gvid_table.append("")
        gvid_table[gvid] = helpers.get_no_module_name(item.get("label"))
    # Populate connections list for each node in graphdict
    for node in tfdata["graphdict"] :
        node_id = gvid_table.index(node.split("-")[0])
        for connection in tfdata["tfgraph"]["edges"] :
            head = connection["head"]
            tail = connection["tail"]
            # Check that the connection is part of the nodes that will be created (exists in graphdict)
            if node_id == head and len([ k for k in tfdata["graphdict"] if k.startswith(gvid_table[tail]) ]) > 0 :
                tfdata["graphdict"][node].append(gvid_table[tail])
    return tfdata
 