﻿# -*- coding: utf-8 -*-
# Copyright (c) 2011 Alexandre Beaulieu <alxbl03@gmail.com>
#
# A simple plugin for Anki that allows to lookup example sentences
# for a given word and automatically add them to a deck.
#
# Example sentences are pulled from www.alc.co.jp

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from aqt import mw, modelchooser, deckchooser
from BeautifulSoup import BeautifulSoup
import urllib, re

class Sentence(QTreeWidgetItem):
    """A sentence that can be imported into Anki."""
    def __init__(self, jp, en):
        super(Sentence, self).__init__()
        self.japanese = jp
        self.english = en
        self.setText(0, jp)
        self.setText(1, en)


class SentenceList(QTreeWidget):
    """Holds multiple example sentences."""
    def __init__(self):
        super(SentenceList, self).__init__()
        self.setColumnCount(2)
        self.setHeaderLabels([u'Front', u'Back',])
        self.setSelectionMode(QAbstractItemView.MultiSelection)

    def add(self, jp, en):
        """Add a sentence to the list."""
        self.addTopLevelItem(Sentence(jp, en))

class SentencePicker(QWidget):
    def __init__(self, parent=None):
        super(SentencePicker, self).__init__(parent)
        self._sentences = SentenceList()
        self._word = QLineEdit()
        self._word.returnPressed.connect(self._search)
        self.initUI()

    def initUI(self):
        # Base window
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle(u'アルクから例文をインポート')
        lMain = QVBoxLayout()
        self.setLayout(lMain)

        # Model picker
        lSettings = QHBoxLayout()
        self._wModel = QWidget()
        self._wDeck  = QWidget()
        lSettings.addWidget(self._wModel)
        lSettings.addWidget(self._wDeck)
        
        self._modelchooser = modelchooser.ModelChooser(mw, self._wModel)
        self._deckchooser  = deckchooser.DeckChooser(mw, self._wDeck)

        # Input dialog
        lInput = QHBoxLayout()
        lInput.addWidget(QLabel(u'言葉:'))
        lInput.addWidget(self._word)
        bSearch = QPushButton(u'検索')
        bSearch.clicked.connect(self._search)
        lInput.addWidget(bSearch)
    
        # Dialog
        bImport = QPushButton(u'カードとしてインポート')
        bImport.clicked.connect(self._import)

        bCancel = QPushButton(u'キャンセル')
        bCancel.clicked.connect(self._cancel)

        lDialog = QHBoxLayout()
        lDialog.addStretch()
        lDialog.addWidget(bImport)
        lDialog.addWidget(bCancel)
    
        # Put the grid together
        lMain.addLayout(lSettings)
        lMain.addLayout(lInput)
        lMain.addWidget(self._sentences, stretch = 1)
        lMain.addLayout(lDialog)

    def _import(self):
        """Import the selected sentences into the active deck."""
        # Show progress dialog
        if self._sentences.topLevelItemCount() == 0 or len(self._sentences.selectedItems()) == 0:
            self._show_error(u'You must select something...')
            return
            
        progress = QProgressDialog(u'例文をインポート中...', u'キャンセル', 0, self._sentences.topLevelItemCount())
        progress.open()
        # Import sentences
        
        # Clear view
        self._sentences.clear()
        self._word.clear()

    def _cancel(self):
        """Cancel import and close window."""
        self._sentences.clear()
        self._word.clear()
        self.hide()

    def _search(self):
        """Search for a specific word and collect example sentences."""
        # Make sure that there is a word input
        if self._word.text() == u'':
            self._show_error(u'検索言葉を入力して下さい。')
            return
        self._sentences.clear()
        progress = QProgressDialog(u'例文を読み込み中...', u'キャンセル', 0, 100)
        progress.open()
        percent = 0
        word = self._word.text()
        url = u'http://eow.alc.co.jp/{0}/UTF-8/?ref=sa'.format(urllib.quote(unicode(self._word.text()).encode('utf-8')))
        percent = 5
        progress.setValue(percent)
        try:
            html = urllib.urlopen(url).read()
        except:
            self._show_error(u'インターネットに接続が出来ませんでした。')
            self._sentences.clear()
            progress.reset()
            return
        percent = 50
        progress.setValue(percent)
        soup = BeautifulSoup(html)
        sentences = soup.find('div', id='resultsList').find('ul')('li', recursive=False)
        for s in sentences:
            jp = re.sub(r'<.*?>', '', unicode(s.span))
            en = re.sub(u'(<.*?>|〔.*)', '', unicode(s.div), re.U)
            percent = percent + (percent/len(sentences))
            progress.setValue(percent)
            self._sentences.add(jp, en)
            
        progress.setValue(100)
        
        
    def _show_error(self, msg):
        error = QMessageBox()
        error.setText(u'エラーが発生しました。')
        error.setInformativeText(msg)
        error.exec_()
        
# Start with alc being None because addons are loaded before the list
# of decks is available.
alc = None 

def show():
    global alc

    if not alc:
        alc = SentencePicker()
    if alc.isHidden():
        alc.show()
    else:
        alc.hide()

a = QAction(mw)
a.setText(u'スペースアルクで例文検索...')
a.setShortcut("F11")
mw.form.menuTools.addAction(a)
mw.connect(a, SIGNAL("triggered()"), show)