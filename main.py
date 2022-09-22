from tkinter import *
from typing import Union
from googletrans import Translator
import pickle
from random import shuffle, getrandbits

options = [
    "Familie",
    "Kultur und Kunst",
    "Sport",
    "Wohnen",
    "Einkäufe und Dienstleistungen",
    "Gesundheitspflege",
    "Reisen",
    "Schule und Studium",
    "Arbeit und Beruf",
    "Zwischenmenschliche Beziehungen",
    "Mensch und Natur",
    "Wissenschaft und Technik",
    "Jugend und Gesellschaft",
    "Kommunikation",
    "Massenmedien",
    "Jugend und ihre Welt",
    "Essen und Trinken",
    "Freizeit",
    "Multikulturelle Gesellschaft",
    "Städte und Orte",
    "Mode und Kleidung",
    "Vorbilde und Idole",
    "Deutschsprachige Länder",
    "Slowakei",
    "Die Europäische Union",
    "Bedeutende Persönlichkeiten",
    "Rest",
    "*Küche"
]


class Array:
    def __init__(self):
        self.array = []

    def append(self, x):
        self.array.append(x)


class Card(object):
    def __init__(self):
        self.origin = ""
        self.translated = ""
        self.use = ""
        self.category = ""
        self.plus_minus = 0

    def insert(self, text1: str, text2=""):
        self.origin = text1
        self.translated = text2

    def translate(self):
        if not self.origin:
            self.translated = t.translate(self.origin, dest="en")

    def edit(self, origin="", translated="", use="", category=""):
        self.origin = origin
        self.translated = translated
        self.use = use
        self.category = category
        self.translate()

    def __str__(self):
        return f"Origin: {self.origin}\n Translated: {self.translated}\n Use: {self.use}\n Category: {self.category}"


class LingoLearn(object):
    def __init__(self, w: Tk):
        self.window = w
        self.newWindow = None
        self.cards = shuffleList(a.array)
        self.window.bind("<Return>", self.check)
        shuffle(self.cards)
        self.index = 0
        self.currentCard = self.cards[self.index]

        self.menuBar = Menu(self.window, background="#14213D", foreground='blue', activebackground='yellow', activeforeground='blue')
        self.fileBar = Menu(self.menuBar, tearoff=0, background='#14213D', foreground='#54AFBC')
        self.fileBar.add_command(label="Save", command=save)
        self.editBar = Menu(self.menuBar, tearoff=0, background='#14213D', foreground='#54AFBC')
        self.editBar.add_command(label="Edit card", command=self.edit)

        self.menuBar.add_cascade(label="File", menu=self.fileBar)
        self.menuBar.add_cascade(label="Edit", menu=self.editBar)
        self.window.config(menu=self.menuBar)

        self.mainLabel = Label(text="Lingo Learn", bd=5, bg="#FCA311", font=("Orator Std", 16))
        self.mainLabel.place(relx=0.5, rely=0.05, anchor=CENTER)

        self.cardLabel = Label(text=self.currentCard.translated, bg="#FCA311")
        self.cardLabel.place(relx=0.5, rely=0.4, anchor=CENTER)
        self.textVar = StringVar()
        self.guessEntry = Entry(textvariable=self.textVar, bd=5)
        self.guessEntry.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.cardPMLabel = Label(text=self.currentCard.plus_minus, bg="#FCA311")
        self.cardPMLabel.place(relx=0.5, rely=0.6, anchor=CENTER)

        self.cat = StringVar()
        self.cat.set("Mensch und Natur")
        self.categoryMenu = OptionMenu(self.window, self.cat, *options)
        self.categoryMenu.place(relx=0.7, rely=0.6, anchor=CENTER)
        self.categoryMenu.config(bg='#54AFBC', activebackground="#187380")
        self.confirmSelectionButton = Button(text="Select", command=self.select, bg="#54AFBC", activebackground="#187380")
        self.confirmSelectionButton.place(relx=0.9, rely=0.6, anchor=CENTER)

        self.addCardButton = Button(text="Add Card", command=lambda temp=None: self.addCard(temp), bg="#FCA311")
        self.addCardButton.place(relx=0.1, rely=0.05, anchor=CENTER)

        self.editButton = Button(text="Edit card", command=self.edit, bg="#54AFBC")
        self.editButton.place(relx=0.1, rely=0.15, anchor=CENTER)

        self.rightButton = Button(text="Control", command=lambda temp=None: self.check(temp), bg="#54AFBC")
        self.rightButton.place(relx=0.2, rely=0.4, anchor=CENTER)

        self.wrongButton = Button(text="I don't know", command=self.gotWrong, bg="#FE5C36")
        self.wrongButton.place(relx=0.2, rely=0.5, anchor=CENTER)

        self.nextButton = Button(text="Next card", command=self.next, bg="#FCA311")
        self.nextButton.place(relx=0.2, rely=0.6, anchor=CENTER)

        self.quitButton = Button(text="Quit game", command=self.end, bg="#FE5C36")
        self.quitButton.place(relx=0.9, rely=0.05, anchor=CENTER)

        self.saveButton = Button(text="Save game", command=save, bg="#54AFBC")
        self.saveButton.place(relx=0.9, rely=0.15, anchor=CENTER)

        self.printButton = Button(text="Print", command=self.callback, bg="#FCA311")
        self.printButton.place(relx=0.9, rely=0.25, anchor=CENTER)

    def update(self) -> None:
        if self.index < len(self.cards):
            self.currentCard = self.cards[self.index]
            self.cardLabel.config(text=self.currentCard.translated)
            self.cardPMLabel.config(text=self.currentCard.plus_minus)
        else:
            save()
            self.cardLabel.config(text="You did it")
            self.cardPMLabel.config(text="Congratulations")

    def select(self):
        self.cards = [card for card in a.array if card.category in self.cat.get() + 'Rest']
        shuffle(self.cards)
        for card in self.cards:
            print(card)
        print(self.index)
        self.update()

    def next(self):
        if self.index <= len(self.cards):
            self.index += 1
            self.update()
        else:
            save()
            self.cardLabel.config(text="You did it")
            self.cardPMLabel.config(text="Congratulations")

    def edit(self):
        self.newWindow = Toplevel(self.window)
        self.newWindow = NewCardForm(self.newWindow, self, edit=True, card=self.currentCard)

    def check(self, context):
        temp = self.guessEntry.get().strip()
        if temp:
            if temp in self.currentCard.origin.strip():
                print("Got right!")
                self.gotRight()
            else:
                print(temp, self.currentCard.origin)
                self.gotWrong()
            self.guessEntry.delete(0, len(temp))

    def gotRight(self):
        self.currentCard.plus_minus += 1
        self.index += 1
        self.update()
        print(len(self.cards) - self.index)

    def gotWrong(self):
        self.currentCard.plus_minus -= 1
        self.index += 1
        self.update()
        self.cards.append(self.currentCard)

    def callback(self):
        print(f"Origin: {self.currentCard.origin}\n"
              f"Translated: {self.currentCard.translated}\n"
              f"Use: {self.currentCard.use}\n"
              f"Category: {self.currentCard.category}")

    def end(self):
        self.window.destroy()
        save()

    def showCard(self):
        if self.currentCard.facing:
            self.cardLabel.config(text=self.currentCard.translated)
        else:
            self.cardLabel.config(text=self.currentCard.origin)
        self.currentCard.facing = False

    def addCard(self, context) -> None:
        self.newWindow = Toplevel(self.window)
        self.newWindow = NewCardForm(self.newWindow, self)


class NewCardForm(object):
    def __init__(self, w: Union[Tk, Toplevel], parent: LingoLearn, edit=False, card=None):
        self.w = w
        self.w.config(bg="#434343")
        self.parent = parent
        self.label1 = Label(self.w, text="Enter origin", bg="#FCA311", width=15).grid(row=0, column=0)
        self.label2 = Label(self.w, text="Enter translated", bg="#FCA311", width=15).grid(row=1, column=0)
        self.label3 = Label(self.w, text="Enter use", bg="#FCA311", width=15).grid(row=2, column=0)
        self.label4 = Label(self.w, text="Enter category", bg="#FCA311", width=15).grid(row=3, column=0)

        self.clicked = StringVar()

        if edit:
            self.w.bind("<Return>", lambda event, c=card: self.edit(c))
            self.clicked.set(card.category)
            self.originEntry = Entry(self.w, bd=5)
            self.originEntry.insert(0, card.origin)
            self.originEntry.grid(row=0, column=1)
            self.translatedEntry = Entry(self.w, bd=5)
            self.translatedEntry.insert(0, card.translated)
            self.translatedEntry.grid(row=1, column=1)
            self.useEntry = Entry(self.w, bd=5)
            self.useEntry.insert(0, card.use)
            self.useEntry.grid(row=2, column=1)
            self.submitButton = Button(self.w, text="Submit", command=lambda temp=card: self.edit(c=card), bg="#54AFBC")

        else:
            self.clicked.set("Mensch und Natur")
            self.w.bind("<Return>", self.submit)
            self.originEntry = Entry(self.w, bd=5)
            self.originEntry.grid(row=0, column=1)
            self.translatedEntry = Entry(self.w, bd=5)
            self.translatedEntry.grid(row=1, column=1)
            self.useEntry = Entry(self.w, bd=5)
            self.useEntry.grid(row=2, column=1)
            self.submitButton = Button(self.w, text="Submit", command=lambda temp=None: self.submit(context=temp), bg="#54AFBC")

        self.categoryMenu = OptionMenu(self.w, self.clicked, *options)
        self.categoryMenu.grid(row=3, column=1)
        self.categoryMenu.config(bg='#54AFBC', activebackground="#187380")

        self.submitButton.grid(row=4, column=0, columnspan=2)

    def edit(self, c: Card):
        for card in a.array:
            if card is c:
                origin = self.originEntry.get()
                translated = self.translatedEntry.get()
                use = self.useEntry.get()
                category = self.clicked.get()
                card.edit(origin, translated, use, category)
                self.parent.update()
                self.w.destroy()
                return

    def submit(self, context):
        temp = Card()
        origin = self.originEntry.get()
        translated = self.translatedEntry.get()
        use = self.useEntry.get()
        category = self.clicked.get()
        for card in self.parent.cards:
            if card.origin == origin:
                self.parent.callback()
                self.w.destroy()
                return
        temp.edit(origin, translated, use, category)
        a.append(temp)
        save()
        self.w.destroy()


def save():
    with open(f'cards.pickle', 'wb') as file:
        pickle.dump(a, file)
    with open(f'cardsbackup.pickle', 'wb') as file:
        pickle.dump(a, file)


def loopThroughCards():
    for card in a.array:
        yield card


def shuffleList(l: list):
    temp = []
    for card in l:
        if card.plus_minus > 5:
            if bool(getrandbits(1)):
                temp.append(card)
        else:
            temp.append(card)
    return temp


t = Translator()
with open(f'cards.pickle', 'rb') as file2:
    a = pickle.load(file2)


def main():
    window = Tk()
    window.geometry("360x400")
    window.title("Lingo Learn")
    window.resizable(1, 0)
    window.config(bg="#434343")
    LingoLearn(window)
    window.mainloop()


if __name__ == '__main__':
    main()
