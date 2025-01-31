from . import _AWS


class _Storage(_AWS):
    _type = "storage"
    _icon_dir = "resource_images/aws/storage"


class Backup(_Storage):
    _icon = "backup.png"


class CloudendureDisasterRecovery(_Storage):
    _icon = "cloudendure-disaster-recovery.png"


class EFSInfrequentaccessPrimaryBg(_Storage):
    _icon = "efs-infrequentaccess-primary-bg.png"


class EFSStandardPrimaryBg(_Storage):
    _icon = "efs-standard-primary-bg.png"


class ElasticBlockStoreEBS(_Storage):
    _icon = "elastic-block-store-ebs.png"


class ElasticFileSystemEFS(_Storage):
    _icon = "elastic-file-system-efs.png"


class FsxForLustre(_Storage):
    _icon = "fsx-for-lustre.png"


class FsxForWindowsFileServer(_Storage):
    _icon = "fsx-for-windows-file-server.png"


class Fsx(_Storage):
    _icon = "fsx.png"


class S3Glacier(_Storage):
    _icon = "s3-glacier.png"


class SimpleStorageServiceS3(_Storage):
    _icon = "simple-storage-service-s3.png"


class SnowballEdge(_Storage):
    _icon = "snowball-edge.png"


class Snowball(_Storage):
    _icon = "snowball.png"


class Snowmobile(_Storage):
    _icon = "snowmobile.png"


class StorageGateway(_Storage):
    _icon = "storage-gateway.png"


class Storage(_Storage):
    _icon = "storage.png"


# Aliases

CDR = CloudendureDisasterRecovery
EBS = ElasticBlockStoreEBS
EFS = ElasticFileSystemEFS
FSx = Fsx
S3 = SimpleStorageServiceS3

# Terraform Resource Mappings
aws_backup_plan = Backup
aws_efs_file_system = ElasticFileSystemEFS
aws_efs = ElasticFileSystemEFS
aws_fsx_lustre_file_system = FsxForLustre
aws_fsx_windows_file_system = FsxForWindowsFileServer
aws_glacier_vault = S3Glacier
aws_s3_bucket = SimpleStorageServiceS3
aws_storagegateway_gateway = StorageGateway
