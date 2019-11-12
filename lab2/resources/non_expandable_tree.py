from PyQt5.QtWidgets import QTreeView, QSizePolicy


class NonExpandableTree(QTreeView):
    def __init__(self, parent, layout, model, doubleClicked):
        super().__init__(parent)

        self.setEnabled(True)
        self.setItemsExpandable(False)
        self.setRootIsDecorated(False)

        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.setSizePolicy(sizePolicy)

        self.setModel(model)
        self.setRootIndex(model.index('/'))

        self.doubleClicked.connect(doubleClicked)

        layout.addWidget(self)
