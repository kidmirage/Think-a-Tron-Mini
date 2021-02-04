from tkinter import Canvas, Label, Entry, Tk, NW, DISABLED, ACTIVE, END, Button, filedialog;
import os
from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas as ReportPage
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab_qrcode import QRCodeImage
import qrcode

window = Tk()
window.title("Create Control Cards")

canvas = Canvas(window, width = 1000, height = 170)
canvas.pack()

DATA_OFFSET = 50

operationLabel = Label(window, text="Operation:")
canvas.create_window(20, DATA_OFFSET+20, window=operationLabel, anchor=NW)

operationText = Entry(window, width=50)
canvas.create_window(80, DATA_OFFSET+20, window=operationText, anchor=NW)

payloadLabel = Label(window, text="Payload:")
canvas.create_window(20, DATA_OFFSET+40, window=payloadLabel, anchor=NW)

payloadText = Entry(window, width=50)
canvas.create_window(80, DATA_OFFSET+40, window=payloadText, anchor=NW)

# Keep track of the current card. We will do 10 cards at a time.
currentCard = 0

# Create lists to keep track of all the card information.
MAX_CARDS = 10
operations = []
payloads = []
for _ in range(0, MAX_CARDS):
    operations.append("")
    payloads.append("")

def clearCards():
    global currentCard, operations, payloads, previousButton

    for i in range(0, MAX_CARDS):
        operations[i]= ""
        payloads[i] = ""

    currentCard = 0
    loadCard(currentCard)
    previousButton["state"] = DISABLED
    canvas.update()
    
def showCardNumber():
    global currentCard
    cardNumberLabel = Label(window, text="Card " + str(currentCard+1) + " of " + str(MAX_CARDS) + "  ")
    canvas.create_window(910, DATA_OFFSET+80, window=cardNumberLabel, anchor=NW)
    
def saveCard(currentCard):
    global operations, payloads
    operations[currentCard] = operationText.get()
    payloads[currentCard] = payloadText.get()
    
def loadCard(currentCard):
    global operations, payloads
    
    operationText.delete(0, END)
    operationText.insert(0, (operations[currentCard]))
    payloadText.delete(0, END)
    payloadText.insert(0, (payloads[currentCard]))
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
canvas.create_window(80, DATA_OFFSET+80, window=nextButton, anchor=NW)
    
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
canvas.create_window(20, DATA_OFFSET+80, window=previousButton, anchor=NW)

def loadPage():
    global currentCard, operations, payloads, previousButton
    
    fullName = filedialog.askopenfilename() 
    fileName = os.path.splitext(fullName)[0]
    with open(fileName + ".txt", "r") as file:
        operations=eval(file.readline())
        payloads=eval(file.readline())
    currentCard = 0;
    loadCard(currentCard)
    previousButton["state"] = DISABLED
    canvas.update()

loadButton = Button(text='Load', command=loadPage)
canvas.create_window(20, 20, window=loadButton, anchor=NW)

def savePage():
    global currentCard, operations, payloads
    
    saveCard(currentCard)
    fullName = filedialog.asksaveasfilename() 
    fileName = os.path.splitext(fullName)[0] 
    with open(fileName+".txt", "w") as file:
        file.write(str(operations)+"\n")
        file.write(str(payloads)+"\n")
    createCardReport(fileName)

def createCardReport(fileName):
    global currentCard, operations, payloads
    
    operationCards = ReportPage(fileName + "_operations.pdf", pagesize=letter)
    xOffset = 30*mm
    yOffset = 25*mm
    card = 0

    # For each card...
    for y in range(4, -1, -1):        
        for x in range(0, 2, 1):

            # Setup for new card.
            firstLinePos = 15*mm
            xPos = x*(89*mm) + xOffset
            yPos = y*(51*mm) + yOffset
            
            # Draw the operation name.
            style = ParagraphStyle('Header')
            style.fontSize=30
            style.leading=30*1.2
            operation=Paragraph(operations[card],style)
            aW =70*mm  # available width and height
            aH = 70*mm
            _, h = operation.wrap(aW, aH)
            firstLinePos -= h/2
            operation.drawOn(operationCards, xPos, yPos+firstLinePos)
            card += 1
    operationCards.save()

    payloadCards = ReportPage(fileName + "_payloads.pdf", pagesize=letter)
    xOffset = 38*mm
    yOffset = 19*mm
    card = 0
    for y in range(4, -1, -1):
        for x in range(1, -1, -1):
            xPos = x*(89*mm) + xOffset
            yPos = y*(51*mm) + yOffset
            qr = QRCodeImage(payloads[card], size=40 * mm, border=0, version=1, error_correction=qrcode.constants.ERROR_CORRECT_H)
            qr.drawOn(payloadCards, xPos, yPos)
            card+=1
    payloadCards.save()

saveButton = Button(text='Save', command=savePage)
canvas.create_window(60, 20, window=saveButton, anchor=NW)

clearButton = Button(text='Clear', command=clearCards)
canvas.create_window(97, 20, window=clearButton, anchor=NW)

# Initialize the screen.
clearCards()
showCardNumber()
window.mainloop()