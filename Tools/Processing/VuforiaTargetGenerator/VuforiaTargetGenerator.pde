/*
 * Image Target generator for Vuforia SDK (Processing version)
 * Based on original sketch by Dario Mazzanti.
 */

int myWidth = 1280;
int myHeight;
float ratio = 4.0 / 3.0;

color[] mycolors = {
  #A6C534, #B3D255, #C0E078, #D2EE92, #E4FBAD,
  #CAD246, #D2DC5C, #D8E673, #E2F084, #ECFA97,
  #9AB8B9, #556F90, #1E4D6C, #2B394B, #2B394B
};

void setup()
{
  myHeight = int(myWidth / ratio);
  size(1280, 960);
  noStroke();
  drawPattern(20, 15);
}

void draw()
{
  // empty: keyboard triggers only
}

void drawPattern(int columns, int rows)
{
  background(0);

  float xIncr = width / float(columns);
  float yIncr = height / float(rows);

  smooth();

  for (float xPos = 0; xPos < width; xPos += xIncr * 2)
  {
    for (float yPos = 0; yPos < height; yPos += yIncr * 2)
    {
      fill(mycolors[int(random(0, mycolors.length))]);
      triangle(xPos, yPos, xPos + xIncr, yPos, xPos + xIncr, yPos + yIncr);

      fill(mycolors[int(random(0, mycolors.length))]);
      triangle(xPos, yPos, xPos, yPos + yIncr, xPos + xIncr, yPos + yIncr);

      fill(mycolors[int(random(0, mycolors.length))]);
      triangle(xPos + xIncr, yPos, xPos + 2 * xIncr, yPos, xPos + xIncr, yPos + yIncr);

      fill(mycolors[int(random(0, mycolors.length))]);
      triangle(xPos + 2 * xIncr, yPos, xPos + xIncr, yPos + yIncr, xPos + 2 * xIncr, yPos + yIncr);

      fill(mycolors[int(random(0, mycolors.length))]);
      triangle(xPos, yPos + yIncr, xPos, yPos + 2 * yIncr, xPos + xIncr, yPos + yIncr);

      fill(mycolors[int(random(0, mycolors.length))]);
      triangle(xPos, yPos + 2 * yIncr, xPos + xIncr, yPos + 2 * yIncr, xPos + xIncr, yPos + yIncr);

      fill(mycolors[int(random(0, mycolors.length))]);
      triangle(xPos + xIncr, yPos + yIncr, xPos + 2 * xIncr, yPos + yIncr, xPos + 2 * xIncr, yPos + 2 * yIncr);

      fill(mycolors[int(random(0, mycolors.length))]);
      triangle(xPos + xIncr, yPos + yIncr, xPos + xIncr, yPos + 2 * yIncr, xPos + 2 * xIncr, yPos + 2 * yIncr);
    }
  }

  for (int i = 0; i < int(1.5 * columns * rows); i++)
  {
    float dotSize = random(xIncr / 10.0, xIncr);
    color col = mycolors[int(random(0, mycolors.length))];
    fill(red(col), green(col), blue(col), 210);
    ellipse(random(width), random(height), dotSize, dotSize);
  }
}

void keyPressed()
{
  if (keyCode == ENTER)
  {
    saveFrame("target####.png");
    return;
  }

  if (key == ' ')
  {
    drawPattern(20, 15);
  }
}
