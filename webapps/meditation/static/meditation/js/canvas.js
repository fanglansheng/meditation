/* == Rain Particle Effect ==
* Generate and render rain particles on a transparent canvas.
* Each rain particle is a sprite and has rendom speed.
* I moved rain to the top when it went out of screen.
*/

// screen width and height
var screenW = 850;
var screenH = 500;//window.innerHeight;

var screenTop = 100;
var screenLeft = 0;

var scene, camera, renderer;

// var video, image, imageContext, texture, mesh;

// particles group
var group;

// totul particle amount 
var particleAmount = 300;

// array to store particles
var particles = new Array();

// array to store each particle speed
var rainSpeed = new Array();

var mouseX = 0, mouseY = 0;

var spritePath = "/static/meditation/res/rain1.png";

// mouse ray
var raycaster = new THREE.Raycaster();
var mouse = new THREE.Vector2();

// pause animation
var isPause = false;

$(document).ready(function(){
 
    // init();
    // // createVideo();
    // createPaticles();
    // animate();


    // document.addEventListener( 'mousemove', onDocumentMouseMove, false );
    // document.addEventListener( 'click', onDocumentMouseClick, false );
    // document.addEventListener( 'touchstart', onDocumentTouchStart, false );
    // document.addEventListener( 'touchmove', onDocumentTouchMove, false );

    // window.addEventListener( 'resize', onWindowResize, false );
                
});



// init the render envoriment
function init(){

    // create webGL scene
    scene = new THREE.Scene();

    // set camera
    camera = new THREE.PerspectiveCamera( 75, screenW/screenH, 0.1, 1000 );
    camera.position.z = 300;

    // set renderer
    renderer = new THREE.CanvasRenderer();
    renderer.setPixelRatio( window.devicePixelRatio );
    // set renderer background color
    renderer.setClearColor( 0x000000, 0 );
    renderer.setSize( screenW, screenH);

    // create canvas
    var canvas = document.getElementById("scene-canvas");
    canvas.appendChild( renderer.domElement );

    // create status, shwo the frame rate at left top corner
    stats = new Stats();
    stats.domElement.style.position = 'absolute';
    stats.domElement.style.top = '0px';
    canvas.appendChild( stats.domElement );
}

var INTERSECTED;
// This will create a loop that causes the renderer 
// to draw the scene 60 times per second.
function animate() {
    
    requestAnimationFrame( animate );
    // camera.position.x += ( mouseX - camera.position.x ) * .5;
    // camera.position.y += ( - mouseY - camera.position.y ) * .05;
    // camera.lookAt( scene.position );

    renderer.render( scene, camera );

    // update stats window to show the frame rate.
    stats.update();

    // // update the picking ray with the camera and mouse position    
    // raycaster.setFromCamera( mouse, camera );   

    // // calculate objects intersecting the picking ray
    // var intersects = raycaster.intersectObjects( scene.children );
    
    // if(intersects.length > 0){
    //     if ( INTERSECTED != intersects[ 0 ].object ) {
           
    //         INTERSECTED = intersects[ 0 ].object;
    //         // world position in screen
    //         var intersectPos = intersects[ 0 ].point;

    //         // get mouseX and intersectX in range[0, screenW]
    //         var mosX = (mouse.x + 1)/2 * screenW;
    //         var intersectX = intersectPos.x + screenW/2;

    //         // set x speed;
    //         if(intersectX - mosX > 0)
    //         {
    //             INTERSECTED.position.x += 5;
    //         }
    //         else
    //         {
    //             INTERSECTED.position.x -= 5;
    //         }
    //         // console.log(INTERSECTED.position);
    //     }

    // } else {
    //     // INTERSECTED.position.x  = Math.random() * 800 - 400;
    //     INTERSECTED = null;
    // }

    updateParicles(isPause);
}

function createPaticles(){
    
    // can be delete; add particles to group
    group = new THREE.Group();
    scene.add( group );

    // create rain sprite
    var sprite = THREE.ImageUtils.loadTexture( spritePath );

    // create rain material 
    var rainMat = new THREE.SpriteMaterial({
        map: sprite,
        blending: THREE.AdditiveBlending,
        color: 0xffff00,
        opacity:0.4
    });

    // create particals
    for ( var i = 0; i < particleAmount; i++ ) {

        // new sprite
        particles[i] = new THREE.Sprite( rainMat );

        var particle = particles[i];

        // set particle positions
        particle.position.x = Math.random() * 800 - 400;
        particle.position.y = Math.random() * 400 - 200;
        particle.scale.x = Math.random() * 5 + 5;//Math.random() + 0.5;
        particle.scale.y = particle.scale.x * 9;//Math.random() * 4 + 5;

        scene.add( particle );

        // set each particle speed
        rainSpeed[i] = new THREE.Vector2(particle.position.x , Math.random() * 10 + 20);
    }

}

function createVideo(){
    video = document.getElementById( 'video' );

    image = document.createElement( 'canvas' );
    image.width = 1920;
    image.height = 1080;

    imageContext = image.getContext( '2d' );
    imageContext.fillStyle = '#000000';
    imageContext.fillRect( 0, 0, 1920, 1080 );

    texture = new THREE.Texture( image );

    var material = new THREE.MeshBasicMaterial( { map: texture, overdraw: 0.5 } );
    var plane = new THREE.PlaneGeometry( 480, 204, 4, 4 );

    mesh = new THREE.Mesh( plane, material );
    mesh.scale.x = mesh.scale.y = mesh.scale.z = 1.5;
    scene.add(mesh);
    
}

function updateParicles(isPause){
    if (isPause) return;

    // particle animation: 
    // reset particle position to the top when it hits bottom
    for ( var i = 0; i < particleAmount; i ++ ) {

        var particle = particles[ i ];
        particle.position.y -= rainSpeed[i].y;

        if (particle.position.y < - screenH / 2) {
            particle.position.y = screenH / 2;
            // particle.position.x = rainSpeed[i].x;
        }
    }

}

function onWindowResize() {

    windowHalfX = window.innerWidth / 2;
    windowHalfY = window.innerHeight / 2;

    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();

    renderer.setSize( window.innerWidth, window.innerHeight );

}

function onDocumentMouseClick( event ){
    isPause = !isPause;
}

function onDocumentMouseMove( event ) {

    event.preventDefault();

    // map intervel from [0,1] to [-1,1]
    mouse.x = ( ( event.clientX - screenLeft ) / screenW ) * 2 - 1;
    mouse.y = - ( ( event.clientY - screenTop) / screenH ) * 2 + 1;
}

function onDocumentTouchStart( event ) {

    if ( event.touches.length === 1 ) {

        event.preventDefault();

        mouseX = event.touches[ 0 ].pageX - windowHalfX;
        mouseY = event.touches[ 0 ].pageY - windowHalfY;

    }

}

function onDocumentTouchMove( event ) {

    if ( event.touches.length === 1 ) {

        event.preventDefault();

        mouseX = event.touches[ 0 ].pageX - windowHalfX;
        mouseY = event.touches[ 0 ].pageY - windowHalfY;

    }

}
