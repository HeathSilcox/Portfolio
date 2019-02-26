// You need to include p5.js before running this code.
// sketch.js
// 15/02/2019
// Heath P. Silcox

const canWidth = 300;
const canHeight = 400;
const platformSize = {
	x: 50,
	y: 15
};
const ballSize = {
	x: 12,
	y: 12
};
const angleSpeed = {
	15: {x: 4, y: -1},
	30: {x: 4, y: -2.5},
	45: {x: 3.5, y: -3.5},
	60: {x: 2.5, y: -4},
	90: {x: 0, y: -4}
};
const numberOfPlatformParts = 2;

let mouseConstrained = canWidth / 2;
let platformPos = {
	x: mouseConstrained,
	y: canHeight - 40
};
let ballPos = {
	x: canWidth / 2,
	y: canHeight - 120
};
let angle = 90;




function setup() {
	createCanvas(canWidth, canHeight);
}

function draw() {
	background(150);
	drawBall();
	drawPlatform();
}

function drawBall() {
	ellipseMode(CENTER);
	ellipse(ballPos.x, ballPos.y, ballSize.x, ballSize.y);

	ballPos.x += angleSpeed[angle].x;
	ballPos.y += angleSpeed[angle].y;

	borderRebound();
}

function drawPlatform() {
	mouseConstrained = constrain(mouseX, platformSize.x / 2, canWidth - platformSize.x / 2);
	rectMode(CENTER);
	rect(mouseConstrained, platformPos.y, platformSize.x, platformSize.y);
}

function whatIsTouched() {
	if (ballPos.x < ballSize.x / 2) {
		return 'left';
	}
	if (ballPos.x > canWidth - ballSize.x / 2) {
		return 'right';
	}
	if (ballPos.y < ballSize.y / 2) {
		return 'top';
	}
	if (ballPos.y > canHeight - ballSize.y / 2) {
		return 'bottom';
	}
	if (isPlatformTouched()) {
		print('rebounds');
		return 'platform';
	}

	return null;
}

function isPlatformTouched() { // a débugger
	if (ballPos.y + ballSize.y / 2 > platformPos.y && ballPos.y + ballSize.y / 2 < platformPos.y + 3) { // si on atteint l'ordonnée de la plateforme, le AND est une sécurité
		if (ballPos.x > platformPos.x / 2  && ballPos.x < platformPos.x + platformPos.x / 2) { // si l'abscisse de la balle est dans l'invervalle de la platformPos.x
			return true;
		}
	}

	return false;
}

function borderRebound() {
	switch (whatIsTouched()) {
		case 'left':
			angleSpeed[angle].x *= -1;
			break;
		case 'right':
			angleSpeed[angle].x *= -1;
			break;
		case 'top':
			angleSpeed[angle].y *= -1;
			break;
		case 'bottom':
			angleSpeed[angle].y *= -1;
			break;
		case 'platform':
			platformRebound();
			break;
		default:
			return null;
			break;
	}
}

function platformRebound() {


}

function rebounds() {

}
