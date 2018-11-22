# from mongoengine import Document, EmbeddedDocument, fields
#
#
# class ToolClass:
#     SINGLETOOL = 'SINGLE TOOL'
#     MULTITOOL = 'MULTI TOOL'
#     SERVICE = 'SERVICE'
#     WOKFLOW = 'WORKFLOW'
#
#
# class ContainerType:
#     DOCKER = 'DOCKER'
#     CONDA = 'CONDA'
#     BIOCONDUCTOR = 'BIOCONDUCTOR'
#     SINGULARITY = 'SINGULARITY'
#
#
# class Container(EmbeddedDocument):
#     tag = fields.StringField(required=True, primary_key=True)
#
#     # Full Tag quay.io / biocontainers / abaca: 1.2 - -python ** /
#     fullTag = fields.StringField(required=True)
#     containerType = fields.StringField()
#     binariesURLs = fields.ListField(fields.StringField(max_length=200), required=False)
#     description = fields.StringField(required=False)
#     size = fields.IntField(required=False)
#     downloads = fields.IntField(required=False)
#     lastUpdate = fields.DateTimeField(required=False)
#     maintainer = fields.ListField(fields.StringField(max_length=200), required=False)
#     containerRecipeURL = fields.StringField(required=False)
#     license = fields.StringField(required=False)
#     softwareURL = fields.StringField(required=False)
#     documentationURL = fields.StringField(required=False)
#     searchText = fields.StringField(required=False)
#
#
# class Descriptor(EmbeddedDocument):
#     descriptorType = fields.StringField()
#     descriptor = fields.StringField()
#     descriptorURL = fields.StringField()
#
#
# class ToolVersion(Document):
#     id = fields.StringField(required=True, primary_key=True)
#     vars()['class'] = fields.StringField(verbose_name="class", required=True)
#     name = fields.StringField(required=True)
#     version = fields.StringField(required=True)
#     description = fields.StringField(required=False)
#     urlHome = fields.StringField(required=False)
#     docURL = fields.StringField(required=False)
#     containIds = fields.ListField(fields.StringField(max_length=200), required=False)
#     containerImages = fields.EmbeddedDocumentListField(Container, required=True)
#     descriptors = fields.EmbeddedDocumentListField(Descriptor, required=False)
#     lastUpdate = fields.StringField(required=True)
#     searchText = fields.StringField(required=True)
#     downloads = fields.StringField(required=True)
#     toolClasses = fields.ListField(fields.StringField(max_length=200))
#
#
# class Tool(Document):
#     id = fields.StringField(required=True, primary_key=True)
#     vars()['class'] = fields.StringField(verbose_name="class", required=True)
#     name = fields.StringField(required=True)
#     description = fields.StringField(required=False)
#     urlHome = fields.StringField(required=False)
#     latestVersion = fields.StringField(required=False)
#     toolClasses = fields.ListField(fields.StringField(max_length=10), required=False)
#     organization = fields.ListField(required=False)
#     author = fields.StringField(required=False)
#     containIds = fields.ListField(fields.StringField(max_length=200), required=False)
#     hasChecker = fields.BooleanField(required=False)
#     checkerURL = fields.StringField(required=False)
#     isVerified = fields.BooleanField(required=False)
#     verifiedSource = fields.StringField(required=False)
#     toolVersions = fields.ListField(fields.IntField(), required=True)
#     additionalIdentifiers = fields.ListField(fields.StringField(max_length=200), required=False)
#     registryURL = fields.StringField(required=False)
#     license = fields.StringField(required=False)
