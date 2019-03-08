class ExperimentConfiguration:
    def __init__(
            self,
            description = "",
            algorithmConfiguration = None,
            partitionMethod = "",
            date = ""
    ):
        self.description = description
        self.algorithmConfiguration = algorithmConfiguration
        self.partitionMethod = partitionMethod
        self.date = date