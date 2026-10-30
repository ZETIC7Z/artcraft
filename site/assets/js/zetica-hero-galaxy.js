/**
 * ZETICA 3D Hero Galaxy Engine
 * Faithful port of storytold/artcraft hero-galaxy.tsx & hero-galaxy-tunables.ts
 * Featuring Archimedean spiral arms, 12-tap Poisson blur nebula, 3D card bowing,
 * chromatic dispersion, video textures, idle conveyor drift, and mouse parallax.
 */

(function () {
  'use strict';

  function initGalaxy() {
    const canvas = document.getElementById('hero-galaxy-canvas') || document.querySelector('#hero canvas');
    if (!canvas) {
      console.warn('Hero galaxy canvas not found');
      return;
    }

    const container = canvas.parentElement;
    if (!container) return;

    // Dimensions
    let width = container.clientWidth || window.innerWidth;
    let height = container.clientHeight || window.innerHeight;

    // Three.js Scene, Camera, Renderer
    const scene = new THREE.Scene();
    const FOV = 30;
    const camera = new THREE.PerspectiveCamera(FOV, width / height, 1, 10000);
    
    // 1 world unit == 1 CSS pixel at z = 0
    function updateCamera() {
      const cz = (height / 2) / Math.tan((FOV * Math.PI / 180) / 2);
      camera.position.set(0, 0, cz);
      camera.lookAt(0, 0, 0);
    }
    updateCamera();

    const renderer = new THREE.WebGLRenderer({
      canvas: canvas,
      alpha: true,
      antialias: true,
      powerPreference: 'high-performance'
    });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
    renderer.setSize(width, height);

    // Root Group for rotation and parallax tilt
    const galaxyGroup = new THREE.Group();
    scene.add(galaxyGroup);

    // Color theme detection
    function isDarkMode() {
      return document.documentElement.getAttribute('data-theme') === 'dark' ||
             window.matchMedia('(prefers-color-scheme: dark)').matches;
    }

    // Geometry Tunables matching shipped hero-galaxy-tunables.ts
    const ARMS = 6;
    const TURNS = 1.05;
    const R_MAX_FRAC = 0.68;
    const BIRTH_FRAC = 0.14; // Clean breathing room around the central wordmark
    const CARD_COUNT = 30;

    function getRadii() {
      const diag = Math.hypot(width, height);
      const rMax = diag * R_MAX_FRAC;
      const rBirth = rMax * BIRTH_FRAC;
      return { rMax, rBirth };
    }

    // Shaders from hero-galaxy.tsx
    const CARD_VERT = `
      uniform float uCurve;
      uniform float uWarp;
      uniform vec2 uMouse;
      uniform vec2 uSize;
      varying vec2 vUv;
      void main() {
        vUv = uv;
        vec4 world = modelMatrix * vec4(position, 1.0);
        float d2 = dot(position.xy, position.xy);
        world.z += uCurve * (0.25 - d2) * 2.0;
        vec2 dpx = (position.xy - uMouse) * uSize;
        float rr = max(uSize.x, uSize.y) * 0.6;
        world.z += uWarp * exp(-dot(dpx, dpx) / max(1.0, rr * rr));
        gl_Position = projectionMatrix * viewMatrix * world;
      }
    `;

    const CARD_FRAG = `
      uniform sampler2D uMap;
      uniform vec3 uBg;
      uniform float uBlur;
      uniform float uAlpha;
      uniform float uAber;
      uniform vec2 uSize;
      uniform float uRadius;
      uniform vec3 uFrameCol;
      uniform float uFrameA;
      varying vec2 vUv;

      const vec2 TAPS[12] = vec2[12](
        vec2(-0.326, -0.406), vec2(-0.840, -0.074), vec2(-0.696, 0.457),
        vec2(-0.203, 0.621), vec2(0.962, -0.195), vec2(0.473, -0.480),
        vec2(0.519, 0.767), vec2(0.185, -0.893), vec2(0.507, 0.064),
        vec2(0.896, 0.412), vec2(-0.322, -0.933), vec2(-0.792, -0.598)
      );

      void main() {
        vec2 uv = vUv;
        vec3 col;
        if (uBlur > 0.002) {
          float a = fract(sin(dot(gl_FragCoord.xy, vec2(12.9898, 78.233))) * 43758.545) * 6.2832;
          mat2 rot = mat2(cos(a), -sin(a), sin(a), cos(a));
          vec3 acc = texture2D(uMap, uv).rgb;
          for (int i = 0; i < 12; i++) {
            acc += texture2D(uMap, clamp(uv + rot * TAPS[i] * uBlur, 0.0, 1.0)).rgb;
          }
          col = acc / 13.0;
        } else {
          vec2 d = uv - 0.5;
          vec2 shift = d * dot(d, d) * 4.0 * uAber;
          col = vec3(
            texture2D(uMap, clamp(uv + shift, 0.0, 1.0)).r,
            texture2D(uMap, uv).g,
            texture2D(uMap, clamp(uv - shift, 0.0, 1.0)).b
          );
        }

        // Rounded-rect SDF in card px
        vec2 q = abs((vUv - 0.5) * uSize) - (0.5 * uSize - vec2(uRadius));
        float dEdge = length(max(q, vec2(0.0))) + min(max(q.x, q.y), 0.0) - uRadius;
        float frameBand = 1.0 - smoothstep(0.5, 1.5, abs(dEdge + 1.0));
        col = mix(col, uFrameCol, frameBand * uFrameA);
        float aa = 1.0 - smoothstep(-0.75, 0.75, dEdge);
        gl_FragColor = vec4(col, uAlpha * aa);
      }
    `;

    // 1. Create Underlay Guide Curves and Ticks
    const underlayGroup = new THREE.Group();
    galaxyGroup.add(underlayGroup);

    let guideLines = [];
    let tickLines = [];

    function buildUnderlay() {
      while (underlayGroup.children.length > 0) {
        const obj = underlayGroup.children[0];
        underlayGroup.remove(obj);
        if (obj.geometry) obj.geometry.dispose();
      }

      const { rMax, rBirth } = getRadii();
      const dark = isDarkMode();
      const lineCol = dark ? 0xffffff : 0x000000;
      const lineMat = new THREE.LineBasicMaterial({
        color: lineCol,
        transparent: true,
        opacity: dark ? 0.12 : 0.08
      });
      const tickMat = new THREE.LineBasicMaterial({
        color: lineCol,
        transparent: true,
        opacity: dark ? 0.22 : 0.15
      });

      // Spiral Arms
      const thetaBirth = BIRTH_FRAC * (TURNS * Math.PI * 2);
      const thetaExit = TURNS * Math.PI * 2;
      const b = (rMax - rBirth) / (thetaExit - thetaBirth);

      for (let j = 0; j < ARMS; j++) {
        const phase = (j * Math.PI * 2) / ARMS;
        const pts = [];
        const tickPts = [];
        const steps = 120;

        for (let k = 0; k <= steps; k++) {
          const t = thetaBirth + (k / steps) * (thetaExit - thetaBirth);
          const r = rBirth + b * (t - thetaBirth);
          const a = t + phase;
          const x = r * Math.cos(a);
          const y = r * Math.sin(a);
          pts.push(new THREE.Vector3(x, y, -2));

          // Ticks every 4 steps
          if (k > 5 && k % 4 === 0) {
            const dx = Math.cos(a + Math.PI / 2) * 6;
            const dy = Math.sin(a + Math.PI / 2) * 6;
            tickPts.push(new THREE.Vector3(x - dx, y - dy, -1.9));
            tickPts.push(new THREE.Vector3(x + dx, y + dy, -1.9));
          }
        }

        const geo = new THREE.BufferGeometry().setFromPoints(pts);
        const line = new THREE.Line(geo, lineMat);
        underlayGroup.add(line);

        if (tickPts.length > 0) {
          const tGeo = new THREE.BufferGeometry().setFromPoints(tickPts);
          const tSeg = new THREE.LineSegments(tGeo, tickMat);
          underlayGroup.add(tSeg);
        }
      }

      // Construction Circle around birth radius
      const circlePts = [];
      const cSteps = 64;
      for (let i = 0; i <= cSteps; i++) {
        const ca = (i / cSteps) * Math.PI * 2;
        circlePts.push(new THREE.Vector3(rBirth * Math.cos(ca), rBirth * Math.sin(ca), -2));
      }
      const cGeo = new THREE.BufferGeometry().setFromPoints(circlePts);
      const cLine = new THREE.Line(cGeo, lineMat);
      underlayGroup.add(cLine);
    }

    buildUnderlay();

    // 2. Preload Artwork Stills for immediate, rich visuals on every card
    const artworkSources = [
      './assets/images/artcraft-commercial-a1eede0a.png',
      './assets/images/artcraft-sci-fi-4ab5c5c7.png',
      './assets/images/artcraft-pirate-3cd9b827.png',
      './assets/images/artcraft-knight-pose-0f2ecb96.png',
      './assets/images/artcraft-worldlabs-ad-a78c82db.png',
      './assets/images/hqdefault-4f6f0b5c.jpg',
      './assets/images/hqdefault-487e8299.jpg',
      './assets/images/hqdefault-e8ad1523.jpg',
      './assets/images/maxresdefault-a4afd56d.jpg',
      './assets/images/organize-93cd9515.webp',
      './assets/images/prototype-6cffaf11.webp',
      './assets/images/dashboard-8f832127.webp',
      './assets/images/swatches-0134b861.webp',
      './assets/images/layout-492a2f03.webp',
      './assets/images/layer-styles-cdd2ab1a.webp',
      './assets/images/masking-7daa0f24.webp'
    ];

    const textureLoader = new THREE.TextureLoader();
    const artworkTextures = artworkSources.map(src => {
      const tex = textureLoader.load(src);
      tex.minFilter = THREE.LinearFilter;
      tex.magFilter = THREE.LinearFilter;
      return tex;
    });

    // Load Video Textures
    const videoSources = [
      './videos/features/WorldLabs_Demo_2.webm',
      './videos/features/Panel.webm',
      './videos/features/Editor.webm',
      './videos/features/Make_3D.webm',
      './videos/features/Mixed.webm',
      './videos/features/Character-Pose.webm',
      './videos/features/Background.webm'
    ];

    const videoElements = [];
    const videoTextures = [];

    videoSources.forEach((src) => {
      const vid = document.createElement('video');
      vid.src = src;
      vid.crossOrigin = 'anonymous';
      vid.loop = true;
      vid.muted = true;
      vid.playsInline = true;
      vid.autoplay = true;
      vid.style.display = 'none';
      document.body.appendChild(vid);

      vid.play().catch(() => {
        const resume = () => {
          vid.play();
          window.removeEventListener('pointerdown', resume);
        };
        window.addEventListener('pointerdown', resume);
      });

      const tex = new THREE.VideoTexture(vid);
      tex.minFilter = THREE.LinearFilter;
      tex.magFilter = THREE.LinearFilter;
      tex.format = THREE.RGBAFormat;

      videoElements.push(vid);
      videoTextures.push(tex);
    });

    // Procedural Fallback Textures for young / loading cards
    function createProceduralTexture(seed) {
      const c = document.createElement('canvas');
      c.width = 256;
      c.height = 144;
      const ctx = c.getContext('2d');
      const grad = ctx.createLinearGradient(0, 0, 256, 144);
      const hue1 = (seed * 67) % 360;
      const hue2 = (hue1 + 45) % 360;
      grad.addColorStop(0, `hsl(${hue1}, 75%, 45%)`);
      grad.addColorStop(1, `hsl(${hue2}, 85%, 25%)`);
      ctx.fillStyle = grad;
      ctx.fillRect(0, 0, 256, 144);

      // Fine grid texture
      ctx.strokeStyle = 'rgba(255,255,255,0.12)';
      ctx.lineWidth = 1;
      for (let x = 0; x < 256; x += 16) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, 144);
        ctx.stroke();
      }
      for (let y = 0; y < 144; y += 16) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(256, y);
        ctx.stroke();
      }

      const tex = new THREE.CanvasTexture(c);
      tex.minFilter = THREE.LinearFilter;
      return tex;
    }

    const proceduralTextures = Array.from({ length: 8 }, (_, i) => createProceduralTexture(i));

    // 3. Card Instances along Spiral
    const cards = [];
    const cardGroup = new THREE.Group();
    galaxyGroup.add(cardGroup);

    const cardPlaneGeo = new THREE.PlaneGeometry(1, 1, 16, 16);

    for (let i = 0; i < CARD_COUNT; i++) {
      const armIndex = i % ARMS;
      // Stagger progress from 0 (birth) to 1 (exit)
      const p = (i / CARD_COUNT);
      // Alternate artwork stills and video textures
      const tex = (i % 2 === 0 && videoTextures.length > 0)
        ? videoTextures[(i / 2) % videoTextures.length]
        : artworkTextures[i % artworkTextures.length];

      const mat = new THREE.ShaderMaterial({
        vertexShader: CARD_VERT,
        fragmentShader: CARD_FRAG,
        uniforms: {
          uMap: { value: tex },
          uBg: { value: new THREE.Vector3(0.05, 0.05, 0.05) },
          uBlur: { value: 0.1 },
          uAlpha: { value: 0.9 },
          uAber: { value: 0.035 },
          uSize: { value: new THREE.Vector2(100, 100) },
          uRadius: { value: 10.0 },
          uFrameCol: { value: new THREE.Vector3(0.9, 0.9, 0.9) },
          uFrameA: { value: 0.4 },
          uCurve: { value: 16.0 },
          uWarp: { value: 0.0 },
          uMouse: { value: new THREE.Vector2(0, 0) }
        },
        transparent: true,
        depthWrite: false
      });

      const mesh = new THREE.Mesh(cardPlaneGeo, mat);
      cardGroup.add(mesh);

      cards.push({
        mesh: mesh,
        mat: mat,
        arm: armIndex,
        p: p,
        seed: i,
        tex: tex
      });
    }

    // 4. Pointer & Motion Physics
    let mouse = { x: 0, y: 0, targetX: 0, targetY: 0 };
    let scrollY = window.scrollY || 0;
    let targetScrollY = scrollY;

    window.addEventListener('mousemove', (e) => {
      mouse.targetX = (e.clientX - width / 2);
      mouse.targetY = -(e.clientY - height / 2);
    });

    window.addEventListener('scroll', () => {
      targetScrollY = window.scrollY || 0;
    }, { passive: true });

    // 5. Render Loop
    let lastTime = performance.now();
    let globalAngle = 0;
    let conveyorOffset = 0;

    function animate(now) {
      requestAnimationFrame(animate);

      const dt = Math.min((now - lastTime) / 1000, 0.1);
      lastTime = now;

      // Idle conveyor advance: 0.57 cycles per minute
      conveyorOffset += (dt * 0.57) / 60;

      // Scroll scrub: 0.2 journeys per 1000px
      const dScroll = targetScrollY - scrollY;
      scrollY += dScroll * 0.1;
      const scrollConveyor = (scrollY / 1000) * 0.2;

      // Global slow rotation: -50 deg/min
      globalAngle += dt * (-50 * (Math.PI / 180) / 60);

      // Mouse Parallax with smooth critically damped spring
      mouse.x += (mouse.targetX - mouse.x) * (1 - Math.exp(-6 * dt));
      mouse.y += (mouse.targetY - mouse.y) * (1 - Math.exp(-6 * dt));

      galaxyGroup.rotation.x = (mouse.y / height) * 0.14;
      galaxyGroup.rotation.y = (mouse.x / width) * 0.14;
      galaxyGroup.rotation.z = globalAngle;

      const { rMax, rBirth } = getRadii();
      const thetaBirth = BIRTH_FRAC * (TURNS * Math.PI * 2);
      const thetaExit = TURNS * Math.PI * 2;
      const b = (rMax - rBirth) / (thetaExit - thetaBirth);

      const dark = isDarkMode();
      const frameCol = dark ? new THREE.Vector3(0.85, 0.85, 0.85) : new THREE.Vector3(0.2, 0.2, 0.2);
      const bgCol = dark ? new THREE.Vector3(0.05, 0.05, 0.05) : new THREE.Vector3(0.98, 0.98, 0.98);

      // Update Cards
      cards.forEach((card) => {
        // Effective journey progress
        let progress = (card.p + conveyorOffset + scrollConveyor) % 1.0;
        if (progress < 0) progress += 1.0;

        const theta = thetaBirth + progress * (thetaExit - thetaBirth);
        const r = rBirth + b * (theta - thetaBirth);
        const phase = (card.arm * Math.PI * 2) / ARMS;
        const a = theta + phase;

        // Subtle floating noise
        const wobble = Math.sin(now * 0.0015 + card.seed * 2.1) * 6;
        const x = (r + wobble) * Math.cos(a);
        const y = (r + wobble) * Math.sin(a);

        card.mesh.position.set(x, y, 10 + progress * 20);

        // Cards stay upright relative to the screen (counter-rotate globalAngle)
        card.mesh.rotation.z = -globalAngle;

        // Sizing & Aspect ratio morphing
        // Newborn cards: square (1:1) and small (~70px); outer cards: 16:9 and large (~280px)
        const aspectFrac = Math.min(1.0, progress / 0.25);
        const currentAspect = 1.0 + aspectFrac * (16 / 9 - 1.0);
        const baseH = 65 + progress * 140;
        const baseW = baseH * currentAspect;

        card.mesh.scale.set(baseW, baseH, 1);

        // Blur & Aberration
        const blurFrac = Math.max(0, 1.0 - progress / 0.22);
        const uBlur = blurFrac * 0.12;
        const uAber = (1.0 - blurFrac) * 0.035;

        // Alpha fade at extreme edges
        let alpha = 1.0;
        if (progress < 0.05) alpha = progress / 0.05;
        if (progress > 0.85) alpha = Math.max(0, 1.0 - (progress - 0.85) / 0.15);

        // Uniforms
        const u = card.mat.uniforms;
        u.uBg.value = bgCol;
        u.uBlur.value = uBlur;
        u.uAber.value = uAber;
        u.uAlpha.value = alpha * 0.92;
        u.uSize.value.set(baseW, baseH);
        u.uFrameCol.value = frameCol;

        // Local mouse warp
        const dx = (mouse.x - x) / baseW;
        const dy = (mouse.y - y) / baseH;
        u.uMouse.value.set(dx, dy);
        u.uWarp.value = Math.max(0, 1.0 - Math.hypot(dx, dy) * 1.5) * 18.0;
      });

      renderer.render(scene, camera);
    }

    requestAnimationFrame(animate);

    // Resize Handler
    window.addEventListener('resize', () => {
      width = container.clientWidth || window.innerWidth;
      height = container.clientHeight || window.innerHeight;
      camera.aspect = width / height;
      updateCamera();
      camera.updateProjectionMatrix();
      renderer.setSize(width, height);
      buildUnderlay();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initGalaxy);
  } else {
    initGalaxy();
  }
})();
