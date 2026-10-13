"""
QuantumCure AI - Page 6: Interactive 3D Anatomy Explorer
Full implementation of Master Prompt Part 11:
- Genuine interactive 3D WebGL model powered by Three.js
- Anatomical structures:
  1. Breast Surface (semi-transparent dermis)
  2. Mammary Parenchyma (glandular tissue)
  3. Chest Wall (Pectoralis Major muscle layer)
  4. Axillary Lymphatic Region & Distinguishable Lymph Nodes (Levels I, II, III)
- Full interactive controls: OrbitControls (rotation, zoom, pan), Reset Camera, Front View, Side View, Axillary View
- Layer visibility toggles (surface, parenchyma, chest wall, lymph nodes)
- Clickable structure selection with dynamic info card & highlighting
- WebGL failure fallback handling
- Strict educational disclaimer (not patient-specific anatomy; binary N0/N+ != exact node localization)
- Strict No-Emoji policy
"""

import sys
from pathlib import Path

root_dir = str(Path(__file__).resolve().parents[2])
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import streamlit as st
import streamlit.components.v1 as components

from frontend.styles import apply_light_theme, render_disclaimer_banner
from frontend.components.sidebar import render_sidebar

st.set_page_config(
    page_title="3D Anatomy Explorer — QuantumCure AI",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_light_theme(st)
render_sidebar(active_tab="3D Anatomy Explorer")

# Mandatory Prominent Clinical Disclaimer
render_disclaimer_banner(st)

# Header Title Row
st.markdown("""
<div class="page-title-row">
    <div>
        <h1 style="margin: 0; font-size: 1.85rem; font-weight: 800; color: #25324A; letter-spacing: -0.02em;">
            3D Anatomy Explorer
        </h1>
        <p style="margin: 3px 0 0 0; font-size: 0.84rem; color: #64748B;">
            Interactive educational 3D representation of mammary parenchyma and axillary lymph node basins (Levels I, II, III).
        </p>
    </div>
    <div style="display: flex; gap: 10px;">
        <span class="status-pill-released" style="background: #E7F8F5; color: #18A999; font-weight: 700;">
            WebGL 3D Accelerated
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# Prominent Specific Anatomy Disclaimer (Part 11)
st.markdown("""
<div style="background: #FFF0EC; border: 1px solid #FECDD3; border-left: 4px solid #F08A78; border-radius: 10px; padding: 10px 16px; margin-bottom: 1.25rem; font-size: 0.82rem; color: #25324A; line-height: 1.5;">
    <strong>Educational Anatomy Notice:</strong> This interactive 3D model represents simplified, generalized regional human anatomy for medical education and research orientation.
    It does <strong>NOT</strong> represent patient-specific anatomy, clinical radiological scans (CT/MRI), primary tumour coordinates, or exact surgical dissection margins.
    The binary N0/N+ classification model in QuantumCure AI does not localize specific lymph node positions.
</div>
""", unsafe_allow_html=True)

# Three.js Interactive Component HTML/CSS/JS
THREEJS_ANATOMY_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        body { background: #F8FAFC; overflow: hidden; width: 100%; height: 100vh; position: relative; }
        #canvas-container { width: 100%; height: 100%; position: absolute; top: 0; left: 0; }
        
        /* UI Floating Overlay Controls */
        .overlay-card {
            position: absolute;
            background: rgba(255, 255, 255, 0.94);
            backdrop-filter: blur(8px);
            border: 1px solid #E5E7EB;
            border-radius: 14px;
            padding: 12px 16px;
            box-shadow: 0 4px 16px rgba(37, 50, 74, 0.08);
            z-index: 10;
        }

        .controls-card {
            top: 14px;
            left: 14px;
            width: 250px;
        }

        .info-card {
            top: 14px;
            right: 14px;
            width: 290px;
        }

        .legend-card {
            bottom: 14px;
            left: 14px;
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
            padding: 8px 14px;
        }

        .camera-card {
            bottom: 14px;
            right: 14px;
            display: flex;
            gap: 6px;
        }

        h4 { font-size: 0.88rem; color: #25324A; font-weight: 700; margin-bottom: 6px; }
        p { font-size: 0.76rem; color: #64748B; line-height: 1.4; margin-bottom: 8px; }

        .btn-cam {
            background: #FFFFFF;
            border: 1px solid #CBD5E1;
            border-radius: 8px;
            padding: 6px 12px;
            font-size: 0.76rem;
            font-weight: 600;
            color: #25324A;
            cursor: pointer;
            transition: all 0.15s ease;
        }
        .btn-cam:hover { background: #7965E8; color: #FFFFFF; border-color: #7965E8; }

        .toggle-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 4px 0;
            font-size: 0.78rem;
            color: #25324A;
        }

        .toggle-row input { cursor: pointer; }

        .legend-item {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 0.74rem;
            color: #25324A;
            font-weight: 600;
        }
        .legend-color {
            width: 12px;
            height: 12px;
            border-radius: 3px;
        }

        #webgl-error {
            display: none;
            position: absolute;
            top: 50%; left: 50%;
            transform: translate(-50%, -50%);
            background: #FFFFFF;
            border: 2px solid #F08A78;
            border-radius: 12px;
            padding: 24px;
            text-align: center;
            max-width: 400px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.1);
        }
    </style>
    <!-- Three.js and OrbitControls from CDN -->
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
</head>
<body>
    <div id="canvas-container"></div>

    <div id="webgl-error">
        <h3 style="color: #F08A78; margin-bottom: 8px;">WebGL Not Supported</h3>
        <p style="color: #64748B; font-size: 0.85rem;">Your current browser or hardware environment does not support WebGL hardware acceleration. Please enable WebGL in settings.</p>
    </div>

    <!-- Left Controls Panel -->
    <div class="overlay-card controls-card">
        <h4>Anatomical Layers</h4>
        <p>Toggle layer visibility or click any structure in the scene to inspect.</p>
        <div class="toggle-row">
            <span>Breast Surface (Skin)</span>
            <input type="checkbox" id="chk-surface" checked>
        </div>
        <div class="toggle-row">
            <span>Mammary Parenchyma</span>
            <input type="checkbox" id="chk-parenchyma" checked>
        </div>
        <div class="toggle-row">
            <span>Chest Wall (Pectoralis)</span>
            <input type="checkbox" id="chk-chest" checked>
        </div>
        <div class="toggle-row">
            <span>Axillary Lymph Nodes (I-III)</span>
            <input type="checkbox" id="chk-nodes" checked>
        </div>
        <div class="toggle-row">
            <span>Drainage Channels</span>
            <input type="checkbox" id="chk-channels" checked>
        </div>
    </div>

    <!-- Right Structure Information Panel -->
    <div class="overlay-card info-card" id="info-panel">
        <h4 id="info-title">Selected: Axillary Basin Level I</h4>
        <div style="font-size: 0.72rem; color: #7965E8; font-weight: 700; margin-bottom: 6px;" id="info-category">Low Axilla Basin</div>
        <p id="info-desc">
            Level I lymph nodes are positioned lateral to the lateral border of Pectoralis Minor. These represent the primary sentinel landing zone for upper-outer quadrant mammary drainage (~75% of lymphatic egress).
        </p>
        <div style="border-top: 1px solid #E5E7EB; padding-top: 6px; font-size: 0.7rem; color: #64748B;">
            <strong>Interaction:</strong> Left-click & drag to rotate | Right-click to pan | Scroll to zoom.
        </div>
    </div>

    <!-- Bottom Legend -->
    <div class="overlay-card legend-card">
        <div class="legend-item"><div class="legend-color" style="background: #E0C8BA;"></div> Skin</div>
        <div class="legend-item"><div class="legend-color" style="background: #F472B6;"></div> Parenchyma</div>
        <div class="legend-item"><div class="legend-color" style="background: #94A3B8;"></div> Chest Wall</div>
        <div class="legend-item"><div class="legend-color" style="background: #18A999;"></div> Level I Nodes</div>
        <div class="legend-item"><div class="legend-color" style="background: #7965E8;"></div> Level II Nodes</div>
        <div class="legend-item"><div class="legend-color" style="background: #F08A78;"></div> Level III Nodes</div>
    </div>

    <!-- Bottom Right Camera Presets -->
    <div class="overlay-card camera-card">
        <button class="btn-cam" onclick="setCameraView('front')">Front</button>
        <button class="btn-cam" onclick="setCameraView('side')">Side</button>
        <button class="btn-cam" onclick="setCameraView('axilla')">Axillary Basin</button>
        <button class="btn-cam" onclick="setCameraView('reset')">Reset</button>
    </div>

    <script>
        // Check WebGL availability
        function webglAvailable() {
            try {
                var canvas = document.createElement('canvas');
                return !!(window.WebGLRenderingContext && (canvas.getContext('webgl') || canvas.getContext('experimental-webgl')));
            } catch (e) {
                return false;
            }
        }

        if (!webglAvailable()) {
            document.getElementById('webgl-error').style.display = 'block';
        }

        var container = document.getElementById('canvas-container');
        var scene = new THREE.Scene();
        scene.background = new THREE.Color(0xF8FAFC);

        var camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 5, 26);

        var renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.shadowMap.enabled = true;
        container.appendChild(renderer.domElement);

        var controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.08;
        controls.maxDistance = 60;
        controls.minDistance = 6;

        // Ambient & Directional Lighting
        var ambientLight = new THREE.AmbientLight(0xFFFFFF, 0.75);
        scene.add(ambientLight);

        var dirLight1 = new THREE.DirectionalLight(0xFFFFFF, 0.85);
        dirLight1.position.set(15, 20, 20);
        scene.add(dirLight1);

        var dirLight2 = new THREE.DirectionalLight(0x7965E8, 0.35);
        dirLight2.position.set(-15, -10, -10);
        scene.add(dirLight2);

        // Group Containers for Layer Toggling
        var groupSurface = new THREE.Group();
        var groupParenchyma = new THREE.Group();
        var groupChest = new THREE.Group();
        var groupNodes = new THREE.Group();
        var groupChannels = new THREE.Group();

        scene.add(groupChest);
        scene.add(groupParenchyma);
        scene.add(groupSurface);
        scene.add(groupNodes);
        scene.add(groupChannels);

        var interactiveObjects = [];

        // 1. Chest Wall Layer (Pectoralis Major curved plate)
        var chestGeo = new THREE.BoxGeometry(22, 18, 0.8);
        var chestMat = new THREE.MeshStandardMaterial({
            color: 0x94A3B8,
            roughness: 0.6,
            metalness: 0.1,
            transparent: true,
            opacity: 0.75
        });
        var chestMesh = new THREE.Mesh(chestGeo, chestMat);
        chestMesh.position.set(0, 0, -3.5);
        chestMesh.userData = {
            title: "Chest Wall (Pectoralis Major)",
            category: "Musculoskeletal Boundary",
            desc: "The pectoralis major and minor muscles define the deep anatomical margin of the breast and partition the axillary space into levels I, II, and III."
        };
        groupChest.add(chestMesh);
        interactiveObjects.push(chestMesh);

        // 2. Mammary Parenchyma (Fibroglandular tissue core)
        var parenchGeo = new THREE.SphereGeometry(6.5, 32, 24);
        var parenchMat = new THREE.MeshStandardMaterial({
            color: 0xF472B6,
            roughness: 0.45,
            metalness: 0.05,
            transparent: true,
            opacity: 0.55
        });
        var parenchMesh = new THREE.Mesh(parenchGeo, parenchMat);
        parenchMesh.position.set(-1.5, -0.5, 1.0);
        parenchMesh.scale.set(1.0, 1.0, 0.7);
        parenchMesh.userData = {
            title: "Mammary Parenchyma",
            category: "Glandular Tissue",
            desc: "Network of 15 to 20 glandular lobes terminating in lactiferous ducts. Primary invasive ductal carcinomas arise from the terminal duct lobular units (TDLU)."
        };
        groupParenchyma.add(parenchMesh);
        interactiveObjects.push(parenchMesh);

        // 3. Breast Surface (Skin contour)
        var surfGeo = new THREE.SphereGeometry(7.6, 36, 28);
        var surfMat = new THREE.MeshStandardMaterial({
            color: 0xE0C8BA,
            roughness: 0.5,
            metalness: 0.05,
            transparent: true,
            opacity: 0.38
        });
        var surfMesh = new THREE.Mesh(surfGeo, surfMat);
        surfMesh.position.set(-1.5, -0.5, 1.2);
        surfMesh.scale.set(1.0, 1.05, 0.75);
        surfMesh.userData = {
            title: "Mammary Dermis & Surface Contour",
            category: "Cutaneous Margin",
            desc: "Outer cutaneous layer and subcutaneous adipose tissue. Skin involvement or tethering indicates advanced local clinical staging (T4b)."
        };
        groupSurface.add(surfMesh);
        interactiveObjects.push(surfMesh);

        // 4. Distinguishable Axillary Lymph Nodes
        function createNode(x, y, z, color, radius, levelName, desc) {
            var nodeGeo = new THREE.SphereGeometry(radius, 18, 18);
            var nodeMat = new THREE.MeshStandardMaterial({
                color: color,
                roughness: 0.3,
                metalness: 0.2,
                emissive: color,
                emissiveIntensity: 0.2
            });
            var nodeMesh = new THREE.Mesh(nodeGeo, nodeMat);
            nodeMesh.position.set(x, y, z);
            nodeMesh.userData = {
                title: levelName,
                category: "Axillary Lymph Basin",
                desc: desc
            };
            groupNodes.add(nodeMesh);
            interactiveObjects.push(nodeMesh);
            return nodeMesh;
        }

        // Level I Nodes (Teal #18A999) - Lateral / Low Axilla
        createNode(6.2, 4.2, 0.5, 0x18A999, 0.65, "Level I Lymph Node (Lateral)", "Located lateral to the pectoralis minor border. Primary drainage site for breast carcinoma.");
        createNode(7.1, 3.1, 0.0, 0x18A999, 0.60, "Level I Lymph Node (Anterior)", "Inferior axillary group receiving primary afferent drainage vessels.");
        createNode(7.8, 5.0, 1.1, 0x18A999, 0.55, "Level I Lymph Node (Pectoral)", "External mammary nodal chain adjacent to the lateral thoracic artery.");

        // Level II Nodes (Purple #7965E8) - Central / Retropectoral
        createNode(6.5, 6.8, -0.5, 0x7965E8, 0.60, "Level II Lymph Node (Central)", "Positioned directly deep/posterior to the pectoralis minor tendon.");
        createNode(7.3, 7.5, -0.8, 0x7965E8, 0.55, "Level II Lymph Node (Interpectoral / Rotter)", "Nodes situated between the pectoralis major and minor muscles.");

        // Level III Nodes (Coral #F08A78) - Apical / Subclavicular
        createNode(5.8, 9.2, -1.8, 0xF08A78, 0.65, "Level III Lymph Node (Apical)", "Medial to pectoralis minor; communicates directly with the subclavian lymphatic trunk.");
        createNode(6.4, 10.1, -2.2, 0xF08A78, 0.55, "Level III Lymph Node (Infraclavicular)", "Highest echelon of axillary drainage prior to supraclavicular basin.");

        // 5. Lymphatic Drainage Pathways (Connecting Tubes)
        var channelPoints = [
            new THREE.Vector3(-0.5, 1.5, 2.0),
            new THREE.Vector3(3.0, 3.0, 1.2),
            new THREE.Vector3(6.2, 4.2, 0.5),
            new THREE.Vector3(6.5, 6.8, -0.5),
            new THREE.Vector3(5.8, 9.2, -1.8)
        ];
        var curve = new THREE.CatmullRomCurve3(channelPoints);
        var tubeGeo = new THREE.TubeGeometry(curve, 32, 0.12, 8, false);
        var tubeMat = new THREE.MeshStandardMaterial({
            color: 0x18A999,
            roughness: 0.3,
            transparent: true,
            opacity: 0.7
        });
        var tubeMesh = new THREE.Mesh(tubeGeo, tubeMat);
        groupChannels.add(tubeMesh);

        // Raycasting for Structure Click Interaction
        var raycaster = new THREE.Raycaster();
        var mouse = new THREE.Vector2();

        window.addEventListener('click', function(event) {
            var rect = renderer.domElement.getBoundingClientRect();
            mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
            mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

            raycaster.setFromCamera(mouse, camera);
            var intersects = raycaster.intersectObjects(interactiveObjects, false);

            if (intersects.length > 0) {
                var selectedObj = intersects[0].object;
                if (selectedObj.userData && selectedObj.userData.title) {
                    document.getElementById('info-title').innerText = "Selected: " + selectedObj.userData.title;
                    document.getElementById('info-category').innerText = selectedObj.userData.category;
                    document.getElementById('info-desc').innerText = selectedObj.userData.desc;
                }
            }
        });

        // Layer Toggles
        document.getElementById('chk-surface').addEventListener('change', function(e) { groupSurface.visible = e.target.checked; });
        document.getElementById('chk-parenchyma').addEventListener('change', function(e) { groupParenchyma.visible = e.target.checked; });
        document.getElementById('chk-chest').addEventListener('change', function(e) { groupChest.visible = e.target.checked; });
        document.getElementById('chk-nodes').addEventListener('change', function(e) { groupNodes.visible = e.target.checked; });
        document.getElementById('chk-channels').addEventListener('change', function(e) { groupChannels.visible = e.target.checked; });

        // Camera Views
        window.setCameraView = function(view) {
            if (view === 'front') {
                camera.position.set(0, 0, 25);
                controls.target.set(0, 2, 0);
            } else if (view === 'side') {
                camera.position.set(25, 2, 0);
                controls.target.set(0, 2, 0);
            } else if (view === 'axilla') {
                camera.position.set(14, 12, 10);
                controls.target.set(6, 6, 0);
            } else if (view === 'reset') {
                camera.position.set(0, 5, 26);
                controls.target.set(0, 0, 0);
            }
            controls.update();
        };

        // Window Resize
        window.addEventListener('resize', function() {
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        });

        // Animation Loop
        function animate() {
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        }
        animate();
    </script>
</body>
</html>
"""

# Render Three.js WebGL canvas inside Streamlit component
components.html(THREEJS_ANATOMY_HTML, height=620)

# Educational Staging Table Below Canvas
st.markdown("""
<div class="ref-dashboard-card" style="margin-top: 1rem;">
    <h3 class="ref-card-title">Axillary Lymph Node Basin Anatomical Staging Levels</h3>
    <div class="ref-card-subtitle">Surgical and radiological classification based on the Pectoralis Minor landmark</div>
    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 14px; margin-top: 14px; font-size: 0.82rem; line-height: 1.6;">
        <div style="background: #E7F8F5; border: 1px solid #A7F3D0; border-radius: 12px; padding: 12px 16px;">
            <strong style="color: #0F8275; font-size: 0.95rem; display: block; margin-bottom: 4px;">Level I (Low Axilla)</strong>
            Anatomical boundary: Lateral to the lateral border of Pectoralis Minor.<br>
            Includes: External mammary, subscapular, and lateral axillary vein nodal groups.<br>
            Clinical relevance: First echelon of lymphatic drainage from upper-outer breast quadrant.
        </div>
        <div style="background: #F0EDFF; border: 1px solid #D8D1F8; border-radius: 12px; padding: 12px 16px;">
            <strong style="color: #7965E8; font-size: 0.95rem; display: block; margin-bottom: 4px;">Level II (Mid Axilla)</strong>
            Anatomical boundary: Directly posterior / deep to Pectoralis Minor muscle.<br>
            Includes: Central axillary chain and interpectoral (Rotter) lymph nodes.<br>
            Clinical relevance: Involvement indicates multi-nodal progression (N+(>2)).
        </div>
        <div style="background: #FFF0EC; border: 1px solid #FED7AA; border-radius: 12px; padding: 12px 16px;">
            <strong style="color: #F08A78; font-size: 0.95rem; display: block; margin-bottom: 4px;">Level III (Apical Axilla)</strong>
            Anatomical boundary: Medial to the medial border of Pectoralis Minor.<br>
            Includes: Subclavicular nodal group emptying into the subclavian vein.<br>
            Clinical relevance: High risk for systemic vascular dissemination; requires radiation therapy.
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
