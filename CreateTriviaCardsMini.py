from tkinter import Canvas, IntVar, Label, Entry, Frame, Tk, LEFT, NW, DISABLED, ACTIVE, END, Radiobutton, Button, filedialog;
import os
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas as ReportPage
from reportlab.lib.pagesizes import letter
from numpy.random.mtrand import randint
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab_qrcode import QRCodeImage
import qrcode

window = Tk()
window.title("Create Trivia Cards")

canvas = Canvas(window, width = 1000, height = 270)
canvas.pack()

DATA_OFFSET = 50

questionLabel = Label(window, text="Question:")
canvas.create_window(20, DATA_OFFSET+20, window=questionLabel, anchor=NW)
canvas.create_window(60, DATA_OFFSET+40, window=Label(window, text="A:"), anchor=NW)
canvas.create_window(60, DATA_OFFSET+60, window=Label(window, text="B:"), anchor=NW)
canvas.create_window(60, DATA_OFFSET+80, window=Label(window, text="C:"), anchor=NW)
canvas.create_window(60, DATA_OFFSET+100, window=Label(window, text="D:"), anchor=NW)
canvas.create_window(60, DATA_OFFSET+120, window=Label(window, text="E:"), anchor=NW)
canvas.create_window(29, DATA_OFFSET+140, window=Label(window, text="Answer:"), anchor=NW)

questionText = Entry(window, width=150)
canvas.create_window(80, DATA_OFFSET+20, window=questionText, anchor=NW)

aText = Entry(window, width=50)
canvas.create_window(80, DATA_OFFSET+40, window=aText, anchor=NW)

bText = Entry(window, width=50)
canvas.create_window(80, DATA_OFFSET+60, window=bText, anchor=NW)

cText = Entry(window, width=50)
canvas.create_window(80, DATA_OFFSET+80, window=cText, anchor=NW)

dText = Entry(window, width=50)
canvas.create_window(80, DATA_OFFSET+100, window=dText, anchor=NW)

eText = Entry(window, width=50)
canvas.create_window(80, DATA_OFFSET+120, window=eText, anchor=NW)

answer = IntVar()
answerFrame = Frame(window)
Radiobutton(answerFrame, text="A", padx=20, variable=answer, value=1).pack( side = LEFT)
Radiobutton(answerFrame, text="B", padx=20, variable=answer, value=2).pack( side = LEFT)
Radiobutton(answerFrame, text="C", padx=20, variable=answer, value=3).pack( side = LEFT)
Radiobutton(answerFrame, text="D", padx=20, variable=answer, value=4).pack( side = LEFT)
Radiobutton(answerFrame, text="E", padx=20, variable=answer, value=5).pack( side = LEFT)
Radiobutton(answerFrame, text="T", padx=20, variable=answer, value=6).pack( side = LEFT)
Radiobutton(answerFrame, text="F", padx=20, variable=answer, value=7).pack( side = LEFT)
canvas.create_window(80, DATA_OFFSET+140, window=answerFrame, anchor=NW)

# Keep track of the current card. We will do 10 cards at a time.
currentCard = 0

# Create lists to keep track of all the card information.
MAX_CARDS = 10
questions = []
aChoices = []
bChoices =[]
cChoices = []
dChoices = []
eChoices = []
answers = []
for _ in range(0, MAX_CARDS):
    questions.append("")
    aChoices.append("")
    bChoices.append("")
    cChoices.append("")
    dChoices.append("")
    eChoices.append("")
    answers.append(0)
    
def clearCards():
    global currentCard, questions, aChoices, bChoices, cChoices, dChoices, eChoices, answers, previousButton
   
    for i in range(0, MAX_CARDS):
        questions[i]= ""
        aChoices[i] = ""
        bChoices[i] = ""
        cChoices[i] = ""
        dChoices[i] = ""
        eChoices[i] = ""
        answers[i] = 0
    currentCard = 0
    loadCard(currentCard)
    previousButton["state"] = DISABLED
    canvas.update()
    
def showCardNumber():
    global currentCard
    cardNumberLabel = Label(window, text="Card " + str(currentCard+1) + " of " + str(MAX_CARDS) + "  ")
    canvas.create_window(910, DATA_OFFSET+180, window=cardNumberLabel, anchor=NW)
    
def saveCard(currentCard):
    global questions, aChoices, bChoices, cChoices, dChoices, eChoices, answers
    questions[currentCard] = questionText.get()
    aChoices[currentCard] = aText.get()
    bChoices[currentCard] = bText.get()
    cChoices[currentCard] = cText.get()
    dChoices[currentCard] = dText.get()
    eChoices[currentCard] = eText.get()
    answers[currentCard] = answer.get()
    
def loadCard(currentCard):
    global questions, aChoices, bChoices, cChoices, dChoices, eChoices, answers
    
    questionText.delete(0, END)
    questionText.insert(0, (questions[currentCard]))
    aText.delete(0, END)
    aText.insert(0, (aChoices[currentCard]))
    bText.delete(0, END)
    bText.insert(0, (bChoices[currentCard]))
    cText.delete(0, END)
    cText.insert(0, (cChoices[currentCard]))
    dText.delete(0, END)
    dText.insert(0, (dChoices[currentCard]))
    eText.delete(0, END)
    eText.insert(0, (eChoices[currentCard]))
    answer.set(answers[currentCard])
    showCardNumber()
    
def nextCard():
    global currentCard
    saveCard(currentCard)
    if currentCard == 0:
        previousButton["state"] = ACTIVE
    currentCard += 1
    if currentCard == MAX_CARDS-1:
        nextButton["state"] = DISABLED
    loadCard(currentCard)
    canvas.update()
    
nextButton = Button(text='Next', command=nextCard)
canvas.create_window(80, DATA_OFFSET+180, window=nextButton, anchor=NW)
    
def previousCard():
    global currentCard
    saveCard(currentCard)
    if (currentCard == MAX_CARDS-1):
        nextButton["state"] = ACTIVE
    currentCard -= 1;
    if currentCard == 0:
        previousButton["state"] = DISABLED
    loadCard(currentCard)
    canvas.update()
    
previousButton = Button(text='Previous', command=previousCard, state=DISABLED)
canvas.create_window(20, DATA_OFFSET+180, window=previousButton, anchor=NW)

def loadPage():
    global currentCard, questions, aChoices, bChoices, cChoices, dChoices, eChoices, answers, previousButton
    
    fullName = filedialog.askopenfilename() 
    fileName = os.path.splitext(fullName)[0]
    with open(fileName + ".txt", "r") as file:
        questions=eval(file.readline())
        aChoices=eval(file.readline())
        bChoices=eval(file.readline())
        cChoices=eval(file.readline())
        dChoices=eval(file.readline())
        eChoices=eval(file.readline())
        answers=eval(file.readline())
    currentCard = 0;
    loadCard(currentCard)
    previousButton["state"] = DISABLED
    canvas.update()

loadButton = Button(text='Load', command=loadPage)
canvas.create_window(20, 20, window=loadButton, anchor=NW)

def savePage():
    global currentCard, questions, aChoices, bChoices, cChoices, dChoices, eChoices, answers
    
    saveCard(currentCard)
    fullName = filedialog.asksaveasfilename() 
    fileName = os.path.splitext(fullName)[0] 
    with open(fileName+".txt", "w") as file:
        file.write(str(questions)+"\n")
        file.write(str(aChoices)+"\n")
        file.write(str(bChoices)+"\n")
        file.write(str(cChoices)+"\n")
        file.write(str(dChoices)+"\n")
        file.write(str(eChoices)+"\n")
        file.write(str(answers))
    createCardReport(fileName)

def createCardReport(fileName):
    global currentCard, questions, aChoices, bChoices, cChoices, tChoices, fChoices, answers
    
    questionCards = ReportPage(fileName + "_questions.pdf", pagesize=letter)
    xOffset = 25*mm
    yOffset = 25*mm
    card = 0

    # For each card...
    for y in range(4, -1, -1):        
        for x in range(0, 2, 1):
            # Determine how many extra choices above 3 there are.
            extras = 0
            if aChoices[card] != "":
                extras += 1
            if bChoices[card] != "":
                extras += 1
            if cChoices[card] != "":
                extras += 1
            if dChoices[card] != "":
                extras += 1
            if eChoices[card] != "":
                extras += 1
            if (extras > 3):
                extras -= 3
            else:
                extras = 0

            # Setup for new card.
            firstLinePos = 40*mm
            xPos = x*(89*mm) + xOffset
            yPos = y*(51*mm) + yOffset
            
            # Draw the question.
            style = ParagraphStyle('Bigger')
            style.fontSize=12
            question=Paragraph(questions[card],style)
            aW = 70*mm  # available width and height
            aH = 20*mm
            _, h = question.wrap(aW, aH)
            firstLinePos -= h 
            firstLinePos += (extras - 3)*(5*mm)
            question.drawOn(questionCards, xPos, yPos+firstLinePos)
            firstLinePos -= 6*mm
            xPos += 15*mm
            
            # Process the choices.
            choice = aChoices[card]
            if choice != "":
                questionCards.drawString(xPos, yPos+firstLinePos, "a. " + choice)
                firstLinePos -= 6*mm
            choice = bChoices[card]
            if choice != "":
                questionCards.drawString(xPos, yPos+firstLinePos, "b. " + choice)
                firstLinePos -= 6*mm
            choice = cChoices[card]
            if choice != "":
                questionCards.drawString(xPos, yPos+firstLinePos, "c. " + choice)
                firstLinePos -= 6*mm
            choice = dChoices[card]
            if choice != "":
                questionCards.drawString(xPos, yPos+firstLinePos, "d. " + choice)
                firstLinePos -= 6*mm
            choice = eChoices[card]
            if choice != "":
                questionCards.drawString(xPos, yPos+firstLinePos, "e. " + choice)
                firstLinePos -= 6*mm
            if answers[card]==6 or answers[card]==7:
                questionCards.drawString(xPos, yPos+firstLinePos, "True")
                firstLinePos -= 6*mm
                questionCards.drawString(xPos, yPos+firstLinePos, "False")           
                
            card += 1
    questionCards.save()

    answerCards = ReportPage(fileName + "_answers.pdf", pagesize=letter)
    xOffset = 38*mm
    yOffset = 19*mm
    card = 0
    for y in range(4, -1, -1):
        for x in range(1, -1, -1):
            xPos = x*(89*mm) + xOffset
            yPos = y*(51*mm) + yOffset
            qr = QRCodeImage(getCode(answers[card]), size=40 * mm, border=0, version=1, error_correction=qrcode.constants.ERROR_CORRECT_H)
            qr.drawOn(answerCards, xPos, yPos)
            card+=1
    answerCards.save()

# Obfuscate the answer so QR codes are not the same.
def getCode(answer):
    
    answerString = "A"
    firstDigit = randint(0,9)
    answerString += str(firstDigit)
    for i in range(0,10):
        if ((i+firstDigit) % 10) == answer:
            answerString += str(i)
            break
    return answerString   

saveButton = Button(text='Save', command=savePage)
canvas.create_window(60, 20, window=saveButton, anchor=NW)

clearButton = Button(text='Clear', command=clearCards)
canvas.create_window(97, 20, window=clearButton, anchor=NW)

# Initialize the screen.
clearCards()
showCardNumber()
window.mainloop()