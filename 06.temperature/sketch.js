//  06.temperature
// Recreate Coding Train's world temperature visualization
//
/***** ***** ***** ***** ***** ***** ***** ***** ***** *****/
let data; // table temp data
let months; // month names
let zeroRadius = 75
let oneRadius = 200;

/***** ***** ***** ***** ***** ***** ***** ***** ***** *****/


/***** ***** ***** ***** ***** ***** ***** ***** ***** *****/
//function keyPressed() { if (key == "g") { loop(); } }
//function mousePressed() { loop(); }
function preload() {
  data = loadTable("GISSTEMPv4.csv", 'csv', 'header')
}

function setup() {
  createCanvas(800, 600);
  // console.log(data.getRowCount());
  // console.log(data.getColumnCount());

  let row = data.getRow(0);

  //console.log(row.getNum("Year"));
  //console.log(row.getNum("Jan"));
  months =  data.columns.slice(1, 13);
  console.log(months)
}

function draw() {
  background(200);
  translate (width/2, height/2); // move 0,0 to center
  noFill();
  stroke(255);
  strokeWeight(2);

  stroke(255);
  strokeWeight(2);
  noFill()
  circle(0, 0, zeroRadius);
  fill(255);
  noStroke();
  text("0", 50, 0);

  stroke(255);
  noFill()
  circle(0, 0, 300);
  fill(255);
  noStroke();
  text("1", 150, 0);

  stroke(255);
  strokeWeight(2);
  noFill()
  circle(0, 0, 500);


  for (let i=0; i < months.length; i++) {
    noStroke();
    fill(255);
    textAlign(CENTER);
    textSize(24);
    let angle = map(i, 0, months.length, 0, TWO_PI) + PI/2;
    push();
    let x = 264 * cos(angle);
    let y = 264 * sin(angle);
    translate(x, y);
    rotate(angle + PI/2);
    text(months[i], 0, 0);
    pop();
  }
  beginShape();
  noFill();
  stroke(255);
  for (let j=0; j < data.getRowCount(); j++) { 
    let row = data.getRow(j);
    let year = row.get("Year");
    //textAlign(CENTER, CENTER);
    //text(year, 0, 0);
    for (let i =0; i < months.length; i++) {
      let anomoly = row.getNum(months[i]);
      let angle = map(i, 0, months.length, 0, TWO_PI) + PI/2;
      let r = map(anomoly, 0, 1, zeroRadius, oneRadius);
      let x = r * cos(angle);
      let y = r * sin(angle);
      vertex(x, y);
    }
  }
  //endShape(CLOSE);
  //noLoop();
  currentRow++;
}
