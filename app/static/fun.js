
			function getQueryVariable( variable )
			{
			       var query = window.location.search.substring(1);
			       var vars = query.split("&");
			       for (var i=0;i<vars.length;i++) {
			            var pair = vars[i].split("=");
			            if(pair[0] == variable){return pair[1];}
			       }
			       return(false);
			}

			var supportsWebGL = ( function () { try { return !! window.WebGLRenderingContext && !! document.createElement( 'canvas' ).getContext( 'experimental-webgl' ); } catch( e ) { return false; } } )();

			var screenWidth=0, 
				screenHeight=0, 
				isHappy=true,
				cubeRotX=0, 
				cubeRotY=0, 
				cubeRotXDest= -0.7, 
				cubeRotYDest= -0.7, 
				easeVal=5,
				intervalHandle=0,
				lookOdds=0,
				extraRotDest=0;

			var sceneBG, sceneSquarey,
				camera, renderer,
				planeGeo, planeMaterial, plane,
				glowCubeHolder, glowGeometry, glowMaterial, glowCube,
				geometry, textureCube, textureFace, textureBack,
				materialCube, materialFace, materialBack,
				squareyHolder, squarey,
				composer, pixelatePass, copyPass, blurXPass, blurYPass;


			
			function addEvent(obj, evt, fn) {
				if (obj.addEventListener) {
					obj.addEventListener(evt, fn, false);
				}
				else if (obj.attachEvent) {
					obj.attachEvent("on" + evt, fn);
				}
			}


            
            function getScreenSize() {
				screenWidth = (document.documentElement)?document.documentElement.clientWidth:window.innerWidth;
                screenHeight = (document.documentElement)?document.documentElement.clientHeight:window.innerHeight;
                var myloc = document.getElementById("face");
				screenWidth1 = (myloc)?myloc.clientWidth:window.innerWidth;
				screenHeight1 = 300;
			}

			function onWindowResize() {

				getScreenSize();

				camera.aspect = screenWidth1 / screenHeight1;
				camera.fov = screenHeight1 * 0.045342;
				camera.updateProjectionMatrix();

				renderer.setSize( screenWidth1, screenHeight1 );
				composer.setSize( renderer.domElement.width, renderer.domElement.height );

				if ( screenWidth > screenHeight ) {
					plane.scale.x = screenWidth / 1000;
					plane.scale.y = screenWidth / 1000;
				} else {
					plane.scale.x = screenHeight / 1000;
					plane.scale.y = screenHeight / 1000;
				}
				
				pixelatePass.params.amount = screenWidth1 * 0.1964;
				blurXPass.params.delta.x = blurYPass.params.delta.y = 5 * window.devicePixelRatio;

			}


	        function setPointerPosition(valX, valY) {
	            if ( !isHappy ) {
	            	setHappy();
	            }

	            // set cubeEase values so cube will follow mouse position
	            cubeRotYDest = ( screenWidth / 2 - valX ) / ( screenWidth / 2 ) * -0.7;
	            cubeRotXDest = ( screenHeight / 2 - valY ) / ( screenHeight / 2 ) * -0.7;
	        }


			function lookAround() {

				// check if time to frantically look around
				if ( Math.floor( Math.random() * lookOdds ) == 0 ) {
					// make odds of frantic looking go down
					lookOdds = Math.min( 10, lookOdds + 0.8 );
					// set frantic looking position
					cubeRotXDest = 1 - Math.random() * 2;
					cubeRotYDest = 1 - Math.random() * 2;
				} else {
					// make odds of frantic looking go up
					lookOdds = Math.max( 1, lookOdds - 0.5 );
				}

			}

			function setSad() {
				isHappy = false;
				lookOdds = 5;
				intervalHandle = setInterval( lookAround, 300 );
				extraRotDest += Math.PI;
				TweenLite.to( squarey.rotation, 1, { y: extraRotDest, ease: Elastic.easeOut } )
			}

			function setHappy(){
				isHappy = true;
				if( intervalHandle ) clearInterval( intervalHandle );
				intervalHandle = 0;
				extraRotDest += Math.PI;
				TweenLite.to( squarey.rotation, 1, { y: extraRotDest, ease: Elastic.easeOut } )
			}



			// render to screen
			function render() {

				requestAnimationFrame( render );

				// set cube position
				cubeRotX += ( cubeRotXDest - cubeRotX ) / easeVal;
				cubeRotY += ( cubeRotYDest - cubeRotY ) / easeVal;
				glowCubeHolder.rotation.y = squareyHolder.rotation.y = cubeRotY;
				glowCube.rotation.x = squarey.rotation.x = cubeRotX;
				glowCube.rotation.y = squarey.rotation.y;


				// draw
				composer.reset();
				composer.render( sceneBG, camera );
				composer.pass( blurXPass );
				composer.pass( blurYPass );
				composer.pass( copyPass );
				composer.render( sceneSquarey, camera );
				// composer.pass( pixelatePass );
				composer.toScreen();

			};




			function initWebGL() {

				// browser interaction //////////////////////////////////////

		        var pointerMode = (window.navigator.pointerEnabled)?'pointer':((window.navigator.msPointerEnabled)?'mspointer':(('ontouchstart' in window)?'touch':'mouse'));

		        if ( pointerMode != 'mouse' ) {

		            function onTouchStart( e ) {
		                if( pointerMode == 'mspointer' ) {
		                    setPointerPosition(e.layerX, e.layerY);
		                } else if( pointerMode == 'touch' ) {
		                    e.preventDefault();
		                    setPointerPosition(e.touches[0].pageX, e.touches[0].pageY);
		                }
		            }

		            function onTouchMove( e ) {
		                e.preventDefault();
		                if(pointerMode=='mspointer') {
		                    setPointerPosition(e.layerX, e.layerY);
		                } else {
		                    setPointerPosition(e.touches[0].pageX, e.touches[0].pageY);
		                }
		            }

		            function onTouchEnd( e ) {
		            	if ( isHappy ) setSad();
		            }

		            if(pointerMode=='mspointer') {
		                document.style.msTouchAction='none';
		                document.style.touchAction='none';
		                addEvent(document, 'MSPointerDown', onTouchStart);
		                addEvent(document, 'MSPointerMove', onTouchMove);
		                addEvent(document, 'MSPointerUp', onTouchEnd);
		            } else {
		                addEvent(document, 'touchstart', onTouchStart);
		                addEvent(document, 'touchmove', onTouchMove);
		                addEvent(document, 'touchend',  onTouchEnd);
		            }

		        } else {

		            addEvent(document,'mousemove', function( e ) {
		                setPointerPosition(e.clientX, e.clientY);
		                if ( !isHappy ) setHappy();
		            });
					
		            addEvent(document, "mouseout", function( e ) {
		                e = e ? e : window.event;
		                var from = e.relatedTarget || e.toElement;
		                if (!from || from.nodeName == "HTML") {
		                    if ( isHappy ) setSad();
		                }
		            });
		            
		        }


		        // THREE scene //////////////////////////////////////



				// get & set screen width & height
				getScreenSize();
				// create scene
				sceneBG = new THREE.Scene();
				sceneSquarey = new THREE.Scene();
				// create camera
				camera = new THREE.PerspectiveCamera( screenHeight * 0.045342, screenWidth/screenHeight, 0.1, 1000 );
				camera.position.z = 180;
				// create renderer
				renderer = new THREE.WebGLRenderer( { alpha: true } );
				renderer.setClearColor( 0x000000, 0.0 ); //////////////////////////////////////////////////////////////////////////////////
                renderer.autoClearColor = false;
                
                var myloc2 = document.getElementById("face");
                renderer.setSize( screenWidth, screenHeight );
				myloc2.appendChild( renderer.domElement );


				//create background plane
				planeGeo = new THREE.PlaneGeometry(1000, 1000,1,1);
				planeMaterial = new THREE.MeshBasicMaterial( { map : THREE.ImageUtils.loadTexture('/staticfiles/img/squarey_bg.png') } );
				plane = new THREE.Mesh( planeGeo, planeMaterial);
				sceneBG.add(plane);
				plane.position.z = -800;


				// create the glow (drop shadow) cube
				glowCubeHolder = new THREE.Object3D();
				glowGeometry = new THREE.BoxGeometry( 22, 22, 22 );
				glowMaterial = new THREE.MeshBasicMaterial( { color: 0x000000, opacity: 0.35, transparent:true } );
				glowCube = new THREE.Mesh( glowGeometry, glowMaterial );

				glowCubeHolder.add( glowCube );
				sceneBG.add( glowCubeHolder );


				
				// create textured materials for each cube's faces
				geometry = new THREE.BoxGeometry( 20, 20, 20 );
				textureCube = THREE.ImageUtils.loadTexture('/staticfiles/img/squarey_side.png');
				textureFace = THREE.ImageUtils.loadTexture('/staticfiles/img/squarey_happy.png');
				textureBack = THREE.ImageUtils.loadTexture('/staticfiles/img/squarey_sad.png');

				// render textures at lowest quality
				textureCube.minFilter = textureCube.magFilter = THREE.NearestFilter;
				textureFace.minFilter = textureFace.magFilter = THREE.NearestFilter;
				textureBack.minFilter = textureBack.magFilter = THREE.NearestFilter;

				materialCube = new THREE.MeshBasicMaterial( { map: textureCube } );
				materialFace = new THREE.MeshBasicMaterial( { map: textureFace } );
				materialBack = new THREE.MeshBasicMaterial( { map: textureBack } );

				// set textured materials on each face
		     	var meshFaceMaterial = new THREE.MeshFaceMaterial( [materialCube, materialCube, materialCube, materialCube, materialFace, materialBack] );

				// create squarey cube
				squareyHolder = new THREE.Object3D();
				squarey = new THREE.Mesh( geometry, meshFaceMaterial );

				// add cube to the scene, within a yaw container
				squareyHolder.add( squarey );
				sceneSquarey.add( squareyHolder );


				// postprocessing composer and shader passes
				WAGNER.vertexShadersPath = '/staticfiles/js/libs/vertex-shaders';
				WAGNER.fragmentShadersPath = '/staticfiles/js/libs/fragment-shaders';
				
				composer = new WAGNER.Composer( renderer, { useRGBA: true, minFilter: THREE.NearestFilter, magFilter: THREE.NearestFilter } );
				
				pixelatePass = new WAGNER.PixelatePass();
				pixelatePass.params.amount = 220;
				
				blurXPass = new WAGNER.BoxBlurPass();
				blurYPass = new WAGNER.BoxBlurPass();
				blurXPass.params.delta.x = blurYPass.params.delta.y = 5 * window.devicePixelRatio;
				
				copyPass = new WAGNER.CopyPass();


				// get new window size otherwise scene will act like an image you scale
				addEvent(window, 'resize', onWindowResize, false );
				onWindowResize();
				render();

			};
			



			if ( getQueryVariable( "useflash" ) == 1 || !supportsWebGL ) {
				var flashcontent = document.createElement("flashcontent");
				flashcontent.id = "flashcontent";
				flashcontent.style.height = "100%";
				document.body.appendChild( flashcontent );
				var so = new SWFObject("squarey.swf", "squareySwf", "100%", "100%", "9", "#000000");
				so.addParam("AllowScriptAccess", "always");
				so.write("flashcontent");
				ga('init', 'flash');
			} else if ( supportsWebGL ) {
				initWebGL();
				ga('init', 'webgl');
			} else {
				// not supported. sad face.
			}

			
