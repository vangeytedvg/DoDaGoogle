from PyQt5.QtWidgets import QListWidgetItem


class DodaListItem(QListWidgetItem):
    """
        Sublassing QListWidgetItem so we can add some properties
        we need.
    """

    def __init__(self, owner_name="",
                 owner_kind="",
                 fileid="",
                 filename="",
                 file_kind="",
                 mime_type="",
                 trashed="",
                 created_time="",
                 parents=""):
        """
        Ctor
        :param owner_name:
        :param owner_kind:
        :param fileid:
        :param filename:
        :param file_kind:
        :param mime_type:
        :param trashed:
        :param created_time:
        """
        super(DodaListItem, self).__init__()
        self.owner_name = owner_name
        self.owner_kind = owner_kind
        self.fileid = fileid
        self.filename = filename
        self.file_kind = file_kind
        self.mime_type = mime_type
        self.trashed = trashed
        self.created_time = created_time
        self.parents = parents
