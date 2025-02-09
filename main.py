from PIL import Image,ImageDraw,ImageFont,ImageColor

tileColors={
 "grid":"#bbada0",
   "bg":"#faf8ef",
   "fg":"#776e65",
"score":"#eee4da",
"empty":"#cdc1b4",
     -2:("#d9e3ee","#776e65"),
     -4:("#b1c8e0","#776e65"),
     -8:("#78b9f2","#f9f6f2"),
    -16:("#198edd","#f9f6f2"),
    -32:("#2374e4","#f9f6f2"),
    -64:("#1d22e2","#f9f6f2"),
   -128:("#4f27db","#f9f6f2"),
   -256:("#441ec9","#f9f6f2"),
   -512:("#3a18b3","#f9f6f2"),
  -1024:("#4a18b3","#f9f6f2"),
  -2048:("#5b18a0","#f9f6f2"),
  -4096:("#8218c4","#f9f6f2"),
  -8192:("#ab1ed6","#f9f6f2"),
 -16384:("#ed1adf","#f9f6f2"),
 -32768:("#f00ea8","#f9f6f2"),
 -65536:("#f5077a","#f9f6f2"),
      0:("#504b44","#f9f6f2"),
      1:("#f5f2e7","#776e65"),
      2:("#eee4da","#776e65"),
      4:("#ede0c8","#776e65"),
      8:("#f2b179","#f9f6f2"),
     16:("#f59563","#f9f6f2"),
     32:("#f67c5f","#f9f6f2"),
     64:("#f65e3b","#f9f6f2"),
    128:("#edcf72","#f9f6f2"),
    256:("#edcc61","#f9f6f2"),
    512:("#edc850","#f9f6f2"),
   1024:("#edc53f","#f9f6f2"),
   2048:("#edc22e","#f9f6f2"),
   4096:("#2eed72","#f9f6f2"),
   8192:("#2ef547","#f9f6f2"),
  16384:("#22ff27","#f9f6f2"),
  32768:("#20f7c0","#f9f6f2"),
  65536:("#20f7f0","#f9f6f2"),
 131072:("#3c3a32","#f9f6f2"),
}

FONT_PATH_BOLD="clear-sans-bold.ttf"
FONT_PATH_REGULAR="clear-sans-regular.ttf"

def avg(*values): return sum(values)/len(values)
def hex2rgb(hex): return ImageColor.getrgb(hex)
def rgb2hex(rgb): return "#{:02x}{:02x}{:02x}".format(*rgb)
def avgColor(col1,col2):
    rgb1=hex2rgb(col1)
    rgb2=hex2rgb(col2)
    rgbfinal=(int(avg(c1,c2)) for c1,c2 in zip(rgb1,rgb2))
    return rgb2hex(rgbfinal)

def getTile(value,tileSize):
    if value==None: return tileColors.get("empty","#cdc1b4"),"#ffffff",0
    fontSize=int((tileSize*0.6)/((max(len(str(value)),2)+1.3)*0.33))
    lowerValue=None;
    upperValue=None;
    for num in tileColors:
        if isinstance(num,int):
            if num<value:
                if lowerValue==None or num>lowerValue: lowerValue=num
            elif num>value:
                if upperValue==None or num<upperValue: upperValue=num

    colors=tileColors.get(value)
    if not colors:
        #print(f"Color for {value} not found, averaging colors of {lowerValue} and {upperValue}")
        if lowerValue==None or upperValue==None: return "#ff00ff","#000000",fontSize
        bg=avgColor(tileColors[lowerValue][0],tileColors[upperValue][0])
        fg=avgColor(tileColors[lowerValue][1],tileColors[upperValue][1])
    else:
        bg=colors[0]
        fg=colors[1]
    return bg,fg,fontSize

def drawTile(draw,pos,size,bg,fg,value,fontSize):
    font=ImageFont.truetype(FONT_PATH_BOLD,fontSize)
    draw.rounded_rectangle((pos[0],pos[1],pos[0]+size[0],pos[1]+size[1]),radius=round((3/107)*tileHeight),fill=bg)
    if value==None: return # ----->
    text=str(value)
    bbox=draw.textbbox((pos[0],pos[1]),text,font=font)
    textWidth=bbox[2]-bbox[0]
    textHeight=bbox[3]-bbox[1]
    x=pos[0]+(tileWidth-textWidth)/2
    y=pos[1]+(tileHeight-textHeight)/2-textHeight/2 # Move text vertically to align
    draw.text((x,y),text,font=font,fill=fg)

def getGridSize(grid):
    maxLength=0
    for row in grid:
        if len(row)>maxLength: maxLength=len(row)
    return maxLength,len(grid)

score=3932028
grid=[
[     4,   512,  1024,131072],
[     8,   256,  2048, 65536],
[    16,   128,  4096, 32768],
[    32,    64,  8192, 16384]
]

score=35720
grid=[
[  None,  None,     2,  2048],
[  None,  None,     2,  1024],
[  None,  None,     4,   512],
[  None,     8,    64,   128]
]

gridSize=getGridSize(grid)
print(f"Grid size: {gridSize[0]}x{gridSize[1]}")

canvasWidth,canvasHeight=600,800
gridWidth,gridHeight=500,500
canvasWidth,canvasHeight=1200,1600
gridWidth,gridHeight=1000,1000

def updateSizes():
    global gridWidth,gridHeight,gridSX,gridSY,padding,tileWidth,tileHeight
    padding=canvasWidth/10/max(gridSize[0],gridSize[1])
    totalPaddingX=padding*(gridSize[0]+1);
    totalPaddingY=padding*(gridSize[1]+1);
    availableWidth=gridWidth-totalPaddingX;
    availableHeight=gridHeight-totalPaddingY;
    print(f"Padding: {padding}")
    tileWidth=min(availableWidth/gridSize[0],availableHeight/gridSize[1])
    tileHeight=tileWidth
    print("Tile size: ",(tileWidth,tileHeight))
    gridWidth=totalPaddingX+tileWidth*gridSize[0]
    gridHeight=totalPaddingY+tileHeight*gridSize[1]
    gridSX,gridSY=(canvasWidth-gridWidth)/2,canvasHeight-(canvasWidth-max(gridWidth,gridHeight))/2-gridHeight
    print(f"Grid coords: {gridSX},{gridSY}  {gridWidth}x{gridHeight}")

def drawGame(draw):
    draw.rounded_rectangle((gridSX,gridSY,gridSX+gridWidth,gridSY+gridHeight),radius=(6/107)*tileHeight,fill=tileColors.get("grid","#bbada0"))
    text=str(score)
    scoreLength=max(canvasWidth//15,len(text)*canvasWidth//30+canvasWidth//15)
    draw.rounded_rectangle((canvasWidth-canvasWidth//12-scoreLength,canvasHeight//10,canvasWidth-canvasWidth//12,canvasHeight//6),radius=3*(canvasWidth/600),fill=tileColors.get("grid","#bbada0"))
    pos=(avg(canvasWidth-canvasWidth//12-scoreLength,canvasWidth-canvasWidth//12),int(canvasHeight/7.5))
    font=ImageFont.truetype(FONT_PATH_BOLD,canvasHeight//30)
    bbox=draw.textbbox((pos[0],pos[1]),text,font=font)
    textWidth=bbox[2]-bbox[0]
    textHeight=bbox[3]-bbox[1]
    x=pos[0]-textWidth/2
    y=pos[1]-textHeight/2
    draw.text((x,y),text,font=font,fill="#ffffff")
    font=ImageFont.truetype(FONT_PATH_BOLD,canvasHeight//55)
    bbox=draw.textbbox((pos[0],pos[1]),"SCORE",font=font)
    textWidth=bbox[2]-bbox[0]
    textHeight=bbox[3]-bbox[1]
    x=pos[0]-textWidth/2
    y=pos[1]-textHeight/2
    draw.text((x,y-canvasHeight//40),"SCORE",font=font,fill=tileColors.get("score","#eee4da"))
    font=ImageFont.truetype(FONT_PATH_BOLD,canvasHeight//10)
    draw.text((canvasWidth//12,canvasHeight//16),"2048",font=font,fill=tileColors.get("fg","#776e65"))
    draw.text((canvasWidth//12,canvasHeight//16+canvasHeight//10+canvasHeight//20),"Join the numbers and get to the 2048 tile!",font=ImageFont.truetype(FONT_PATH_REGULAR,canvasHeight//44),fill=tileColors.get("fg","#776e65"))

def drawTiles(draw,grid):
    for y,row in enumerate(grid):
        for x,col in enumerate(row):
            value=grid[y][x]
            print((str(value) if value!=None else "").rjust(7," "),end="|")
            bg,fg,fontSize=getTile(value,tileHeight)
            drawTile(draw,(gridSX+x*tileWidth+padding*(x+1),gridSY+y*tileHeight+padding*(y+1)),(tileWidth,tileHeight),bg,fg,value,fontSize)
        print("\n"+gridSize[0]*"--------")

def drawAll(grid):
    updateSizes()
    image=Image.new("RGB",(canvasWidth,canvasHeight),tileColors.get("bg","#faf8ef"))
    draw=ImageDraw.Draw(image)
    drawGame(draw)
    drawTiles(draw,grid)
    return image

drawAll(grid).show()
