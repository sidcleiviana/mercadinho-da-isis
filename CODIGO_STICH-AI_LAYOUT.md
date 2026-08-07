<!DOCTYPE html>

<html class="light" lang="pt-BR"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Mercadinho Feliz - Dashboard</title>
<!-- Material Symbols -->
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<!-- Tailwind CSS -->
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<!-- Tailwind Config injected from Style Guidance -->
<script id="tailwind-config">
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    "colors": {
                        "on-primary-fixed": "#330d26",
                        "tertiary-container": "#e2d588",
                        "magic-lilac": "#E8D5FF",
                        "outline": "#817379",
                        "surface-container-high": "#e8e8e8",
                        "on-primary-fixed-variant": "#653853",
                        "error-container": "#ffdad6",
                        "surface-container-lowest": "#ffffff",
                        "on-secondary-fixed-variant": "#004d64",
                        "tertiary": "#685f1f",
                        "on-secondary-fixed": "#001f2a",
                        "primary": "#7f4f6b",
                        "inverse-surface": "#2f3131",
                        "surface-variant": "#e2e2e2",
                        "surface-container-low": "#f3f3f4",
                        "on-surface-variant": "#4f4449",
                        "on-tertiary": "#ffffff",
                        "surface-bright": "#f9f9f9",
                        "on-tertiary-container": "#655c1c",
                        "on-secondary-container": "#25667e",
                        "on-tertiary-fixed-variant": "#504707",
                        "error": "#ba1a1a",
                        "secondary-fixed": "#bce9ff",
                        "on-error-container": "#93000a",
                        "tertiary-fixed": "#f1e495",
                        "background": "#f9f9f9",
                        "surface-container": "#eeeeee",
                        "surface-tint": "#7f4f6b",
                        "on-tertiary-fixed": "#201c00",
                        "surface-dim": "#dadada",
                        "surface": "#f9f9f9",
                        "mint-success": "#B4F2D6",
                        "primary-container": "#ffc2e2",
                        "secondary": "#24657d",
                        "on-background": "#1a1c1c",
                        "on-error": "#ffffff",
                        "on-primary": "#ffffff",
                        "primary-fixed": "#ffd8eb",
                        "surface-container-highest": "#e2e2e2",
                        "secondary-fixed-dim": "#93cfea",
                        "on-primary-container": "#7b4c67",
                        "text-ink": "#4A3B52",
                        "primary-fixed-dim": "#f1b5d5",
                        "inverse-on-surface": "#f0f1f1",
                        "outline-variant": "#d3c2c9",
                        "action-orange": "#FF9F43",
                        "secondary-container": "#a6e2fe",
                        "on-secondary": "#ffffff",
                        "tertiary-fixed-dim": "#d4c87c",
                        "inverse-primary": "#f1b5d5",
                        "on-surface": "#1a1c1c"
                    },
                    "borderRadius": {
                        "DEFAULT": "1rem",
                        "lg": "2rem",
                        "xl": "3rem",
                        "full": "9999px"
                    },
                    "spacing": {
                        "stack-gap": "16px",
                        "unit": "8px",
                        "margin-mobile": "16px",
                        "gutter": "24px",
                        "margin-desktop": "40px"
                    },
                    "fontFamily": {
                        "body-md": ["Quicksand", "sans-serif"],
                        "title-md": ["Quicksand", "sans-serif"],
                        "body-lg": ["Quicksand", "sans-serif"],
                        "display-lg": ["Quicksand", "sans-serif"],
                        "headline-lg": ["Quicksand", "sans-serif"],
                        "label-bold": ["Quicksand", "sans-serif"],
                        "headline-lg-mobile": ["Quicksand", "sans-serif"]
                    },
                    "fontSize": {
                        "body-md": ["18px", { "lineHeight": "26px", "fontWeight": "500" }],
                        "title-md": ["24px", { "lineHeight": "32px", "fontWeight": "600" }],
                        "body-lg": ["20px", { "lineHeight": "30px", "fontWeight": "500" }],
                        "display-lg": ["48px", { "lineHeight": "56px", "letterSpacing": "-0.02em", "fontWeight": "700" }],
                        "headline-lg": ["32px", { "lineHeight": "40px", "fontWeight": "700" }],
                        "label-bold": ["16px", { "lineHeight": "20px", "letterSpacing": "0.05em", "fontWeight": "700" }],
                        "headline-lg-mobile": ["28px", { "lineHeight": "34px", "fontWeight": "700" }]
                    }
                }
            }
        }
    </script>
<link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<style>
        /* Toy-like Whimsical Background Pattern */
        .whimsical-bg {
            background-color: #f9f9f9;
            background-image: 
                radial-gradient(circle at 20% 30%, rgba(232, 213, 255, 0.4) 0%, transparent 20%),
                radial-gradient(circle at 80% 70%, rgba(255, 194, 226, 0.4) 0%, transparent 20%),
                radial-gradient(circle at 50% 10%, rgba(188, 233, 255, 0.4) 0%, transparent 15%);
            background-size: 100% 100%;
            background-attachment: fixed;
        }

        /* Chunky Toy Button Base */
        .toy-button {
            position: relative;
            transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: inset 0 3px 6px rgba(255, 255, 255, 0.6), 0 8px 16px rgba(0,0,0,0.1);
        }
        .toy-button:active {
            transform: translateY(6px);
            box-shadow: inset 0 2px 4px rgba(255, 255, 255, 0.6), 0 2px 4px rgba(0,0,0,0.1);
            border-bottom-width: 0px !important;
            margin-bottom: 8px; /* Compensate for lost border */
        }

        /* Glassy Ticket Edge */
        .ticket-edge {
            background-image: radial-gradient(circle at 12px 0, transparent 12px, white 13px);
            background-size: 32px 16px;
            background-repeat: repeat-x;
            background-position: top center;
        }
        
        /* Subtle float animation for icons */
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-8px); }
            100% { transform: translateY(0px); }
        }
        .animate-float {
            animation: float 4s ease-in-out infinite;
        }
    </style>
</head>
<body class="whimsical-bg text-on-surface font-body-md min-h-screen overflow-x-hidden selection:bg-primary-container selection:text-on-primary-container">
<!-- TopAppBar (JSON) -->
<header class="fixed top-0 right-0 left-64 h-20 flex justify-between items-center px-margin-desktop z-50 bg-magic-lilac border-b-4 border-primary rounded-b-lg shadow-lg">
<div class="flex items-center gap-4">
<!-- Brand / Product Name Anchor -->
<h1 class="font-headline-lg text-headline-lg text-on-primary-fixed tracking-tight">
                Olá, Ísis! 🌈
            </h1>
</div>
<div class="flex items-center gap-stack-gap">
<!-- Trailing Actions -->
<div class="flex gap-4">
<button class="bg-surface-container-lowest text-on-primary-fixed-variant px-4 py-2 rounded-lg font-label-bold text-label-bold border-b-4 border-surface-variant hover:scale-105 active:scale-95 transition-all flex items-center gap-2 shadow-sm">
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">stars</span>
                    Nível 5 ⭐️
                </button>
<button class="bg-tertiary-container text-on-tertiary-container px-4 py-2 rounded-lg font-label-bold text-label-bold border-b-4 border-tertiary hover:scale-105 active:scale-95 transition-all flex items-center gap-2 shadow-sm">
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">savings</span>
                    Cofre: $1,250
                </button>
</div>
<!-- Icon Actions -->
<button class="w-12 h-12 rounded-lg bg-surface-container-lowest text-primary border-b-4 border-surface-variant flex items-center justify-center hover:scale-105 active:scale-95 transition-all shadow-sm">
<span class="material-symbols-outlined">notifications</span>
</button>
<!-- Avatar -->
<div class="w-14 h-14 rounded-lg bg-white border-4 border-primary overflow-hidden shadow-md flex-shrink-0 cursor-pointer hover:scale-105 transition-transform">
<img alt="Mascote Buddy" class="w-full h-full object-cover" data-alt="A 3D rendered, highly polished, cute, fuzzy pastel-colored monster mascot smiling warmly. The rendering style is reminiscent of high-end animation studios, featuring soft studio lighting, a glossy finish on its eyes, and a magical, friendly expression. The background is a clean, solid soft pink to fit perfectly within a vibrant, child-friendly user interface." src="https://lh3.googleusercontent.com/aida-public/AB6AXuA_pJoyxk7NlQwlOh_6LWcQ5DTW071oDRzZxBxbWjFmxAPeX1A5vGyOlVgL1bCuwUFCVAiclmJjJeGTz-i7LBbGElokRl6g1iZvo91HcdlegPWfV6qAm701TEXoRhbMq8W7uEBhvxzdQXAvH5JtRYWy0A_c-NKPh8XsJd-9CpDI90NAO4CS1fQCIlgCADWCKJPFVsAWUMbJOvnCWnfv9kFD1vSSNoLh1K_IrvnJ1Uv0UKGaOMffIyOV"/>
</div>
</div>
</header>
<!-- SideNavBar (JSON) -->
<nav class="fixed left-0 top-0 h-full flex flex-col p-4 gap-stack-gap z-40 bg-surface-container-low shadow-[4px_0px_0px_0px_rgba(127,79,107,0.2)] w-64 rounded-r-lg">
<!-- Header / Logo -->
<div class="flex flex-col items-center justify-center py-6 gap-2">
<div class="w-20 h-20 rounded-full bg-primary-container border-4 border-primary shadow-sm flex items-center justify-center overflow-hidden mb-2">
<img alt="Mascote de Animal Fofinho" class="w-full h-full object-cover" data-alt="A vibrant, stylized 3D icon of a cute little grocery store awning with a smiling face on the storefront. The colors are bright pastel pinks, lilacs, and yellows. The lighting is soft and bouncy, creating a high-quality, plastic toy aesthetic perfect for a children's educational application." src="https://lh3.googleusercontent.com/aida-public/AB6AXuAdt7pTEtd4fqLCK130a44HvBmDkJFfubvCoqshGdHBbyERffN91n9fGU70mdvh2RIEjq0drJmUlGLIp9lSOfF0mrqJhcH1MyGYxHl1i6ue3KFTEBpr9NQ6zCBv5MYqM426-iGlUJuLE66RKOPVcnaWpw5wSxGBFH0INmwITa5Z41pZwyrX9jYUCmefjRExF2lXFyTEbuYZaDIuPLYtIDUnkmNVvjRM50Lqp-iS3Cy6PmTARQ8LCf_H"/>
</div>
<h2 class="font-title-md text-title-md text-primary text-center leading-tight">Mercadinho Feliz</h2>
<span class="font-label-bold text-label-bold text-on-surface-variant bg-surface-variant px-3 py-1 rounded-full">Nível do Mercado</span>
</div>
<!-- Navigation Tabs -->
<ul class="flex flex-col gap-2 flex-grow mt-4 overflow-y-auto pr-2" style="scrollbar-width: none;">
<!-- Active Tab: Home (Intent matches Dashboard/Welcome area) -->
<li>
<button class="w-full flex flex-col items-center justify-center bg-primary-container text-on-primary-container rounded-lg border-b-4 border-on-primary-fixed-variant p-4 transition-all scale-105 active:translate-y-1 active:border-b-0 duration-100 shadow-sm cursor-default">
<span class="material-symbols-outlined text-3xl mb-1" style="font-variation-settings: 'FILL' 1;">home</span>
<span class="font-label-bold text-label-bold">Home</span>
</button>
</li>
<!-- Inactive Tabs -->
<li>
<button class="w-full flex flex-col items-center justify-center text-on-surface-variant p-4 rounded-lg hover:bg-primary-fixed hover:text-on-primary-fixed-variant transition-colors group">
<span class="material-symbols-outlined text-3xl mb-1 group-hover:scale-110 transition-transform">shopping_basket</span>
<span class="font-label-bold text-label-bold">Produtos</span>
</button>
</li>
<li>
<button class="w-full flex flex-col items-center justify-center text-on-surface-variant p-4 rounded-lg hover:bg-primary-fixed hover:text-on-primary-fixed-variant transition-colors group">
<span class="material-symbols-outlined text-3xl mb-1 group-hover:scale-110 transition-transform">inventory_2</span>
<span class="font-label-bold text-label-bold">Estoque</span>
</button>
</li>
<li>
<button class="w-full flex flex-col items-center justify-center text-on-surface-variant p-4 rounded-lg hover:bg-primary-fixed hover:text-on-primary-fixed-variant transition-colors group">
<span class="material-symbols-outlined text-3xl mb-1 group-hover:scale-110 transition-transform">point_of_sale</span>
<span class="font-label-bold text-label-bold">Caixa</span>
</button>
</li>
<li>
<button class="w-full flex flex-col items-center justify-center text-on-surface-variant p-4 rounded-lg hover:bg-primary-fixed hover:text-on-primary-fixed-variant transition-colors group">
<span class="material-symbols-outlined text-3xl mb-1 group-hover:scale-110 transition-transform">receipt_long</span>
<span class="font-label-bold text-label-bold">Vendas</span>
</button>
</li>
<li>
<button class="w-full flex flex-col items-center justify-center text-on-surface-variant p-4 rounded-lg hover:bg-primary-fixed hover:text-on-primary-fixed-variant transition-colors group">
<span class="material-symbols-outlined text-3xl mb-1 group-hover:scale-110 transition-transform">face_6</span>
<span class="font-label-bold text-label-bold">Clientes</span>
</button>
</li>
<li>
<button class="w-full flex flex-col items-center justify-center text-on-surface-variant p-4 rounded-lg hover:bg-primary-fixed hover:text-on-primary-fixed-variant transition-colors group">
<span class="material-symbols-outlined text-3xl mb-1 group-hover:scale-110 transition-transform">analytics</span>
<span class="font-label-bold text-label-bold">Relatórios</span>
</button>
</li>
<li>
<button class="w-full flex flex-col items-center justify-center text-on-surface-variant p-4 rounded-lg hover:bg-primary-fixed hover:text-on-primary-fixed-variant transition-colors group">
<span class="material-symbols-outlined text-3xl mb-1 group-hover:scale-110 transition-transform">settings</span>
<span class="font-label-bold text-label-bold">Ajustes</span>
</button>
</li>
</ul>
<!-- Bottom CTA -->
<div class="mt-auto pt-4">
<button class="w-full py-4 rounded-lg bg-tertiary text-on-tertiary font-label-bold text-label-bold border-b-4 border-on-tertiary-fixed-variant active:border-b-0 active:translate-y-1 transition-all shadow-md toy-button">
                Ver Conquistas
            </button>
</div>
</nav>
<!-- Main Content Canvas -->
<main class="ml-64 mt-20 p-margin-desktop min-h-[calc(100vh-5rem)]">
<div class="max-w-7xl mx-auto space-y-gutter">
<!-- Bento Grid: Stats Area -->
<section class="grid grid-cols-1 md:grid-cols-3 gap-gutter">
<!-- Stat Card 1: Meu Cofrinho -->
<div class="bg-tertiary-container rounded-lg p-6 shadow-md border-b-[6px] border-[#c0b368] relative overflow-hidden group cursor-pointer hover:translate-y-[-4px] transition-transform">
<div class="absolute -right-4 -top-4 w-32 h-32 bg-white opacity-20 rounded-full blur-2xl"></div>
<div class="flex justify-between items-start mb-4 relative z-10">
<h3 class="font-title-md text-title-md text-on-tertiary-container">Meu Cofrinho</h3>
<div class="w-12 h-12 rounded-full bg-white flex items-center justify-center shadow-inner">
<span class="material-symbols-outlined text-tertiary text-3xl animate-float" style="font-variation-settings: 'FILL' 1;">savings</span>
</div>
</div>
<div class="relative z-10">
<span class="font-display-lg text-display-lg text-on-tertiary-container drop-shadow-sm">R$ 104,00</span>
</div>
<!-- Decorative sparkles -->
<span class="material-symbols-outlined absolute bottom-4 right-4 text-white opacity-50 text-4xl">arrow_back_ios_new</span>
</div>
<!-- Stat Card 2: Nossos Brinquedos -->
<div class="bg-primary-container rounded-lg p-6 shadow-md border-b-[6px] border-[#d99ebf] relative overflow-hidden group cursor-pointer hover:translate-y-[-4px] transition-transform">
<div class="absolute -left-8 -bottom-8 w-40 h-40 bg-white opacity-20 rounded-full blur-2xl"></div>
<div class="flex justify-between items-start mb-4 relative z-10">
<h3 class="font-title-md text-title-md text-on-primary-container">Nossos Brinquedos</h3>
<div class="w-12 h-12 rounded-full bg-white flex items-center justify-center shadow-inner">
<span class="material-symbols-outlined text-primary text-3xl animate-float" style="animation-delay: 0.5s; font-variation-settings: 'FILL' 1;">toys</span>
</div>
</div>
<div class="relative z-10 flex items-end gap-2">
<span class="font-display-lg text-display-lg text-on-primary-container drop-shadow-sm">2</span>
<span class="font-title-md text-title-md text-on-primary-container mb-2 opacity-80">produtos</span>
</div>
</div>
<!-- Stat Card 3: Amigos no Mercado -->
<div class="bg-secondary-fixed rounded-lg p-6 shadow-md border-b-[6px] border-secondary-fixed-dim relative overflow-hidden group cursor-pointer hover:translate-y-[-4px] transition-transform">
<div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-48 h-48 bg-white opacity-20 rounded-full blur-3xl"></div>
<div class="flex justify-between items-start mb-4 relative z-10">
<h3 class="font-title-md text-title-md text-on-secondary-fixed">Amigos no Mercado</h3>
<div class="w-12 h-12 rounded-full bg-white flex items-center justify-center shadow-inner">
<span class="material-symbols-outlined text-secondary text-3xl animate-float" style="animation-delay: 1s; font-variation-settings: 'FILL' 1;">groups</span>
</div>
</div>
<div class="relative z-10 flex items-end gap-2">
<span class="font-display-lg text-display-lg text-on-secondary-fixed drop-shadow-sm">0</span>
<span class="font-title-md text-title-md text-on-secondary-fixed mb-2 opacity-80">clientes</span>
</div>
</div>
</section>
<!-- Main Layout Split: Action Area & Recent Activity -->
<div class="grid grid-cols-1 lg:grid-cols-12 gap-gutter mt-8">
<!-- Status & Main Action (Left/Large Column) -->
<div class="lg:col-span-7 flex flex-col gap-gutter">
<div class="bg-surface-container-lowest rounded-lg p-10 shadow-lg border-4 border-surface-variant flex flex-col items-center justify-center text-center relative overflow-hidden min-h-[400px]">
<!-- Subtle background decoration -->
<span class="material-symbols-outlined absolute -top-10 -right-10 text-[200px] text-surface-container opacity-50 rotate-12">storefront</span>
<div class="relative z-10 flex flex-col items-center gap-8 w-full max-w-md">
<!-- Status Indicator -->
<div class="inline-flex items-center gap-3 bg-error-container text-on-error-container px-6 py-3 rounded-full font-title-md text-title-md shadow-sm border-2 border-white">
<span class="material-symbols-outlined text-3xl" style="font-variation-settings: 'FILL' 1;">dark_mode</span>
                                Mercado Fechado
                            </div>
<p class="font-body-lg text-body-lg text-on-surface-variant">
                                As prateleiras estão arrumadas! Que tal abrir a loja para novos amigos?
                            </p>
<!-- Massive Action Button (Game UI Style) -->
<button class="w-full toy-button bg-action-orange text-white rounded-lg py-8 px-8 border-b-[8px] border-[#d97c21] flex flex-col items-center justify-center gap-2 group">
<span class="material-symbols-outlined text-5xl mb-2 group-hover:scale-110 transition-transform" style="font-variation-settings: 'FILL' 1;">light_mode</span>
<span class="font-display-lg text-headline-lg font-bold tracking-wide uppercase shadow-black/20" style="text-shadow: 0 2px 4px rgba(0,0,0,0.2);">✨ Abrir Mercado</span>
</button>
</div>
</div>
</div>
<!-- Recent Activity / Magic Receipt (Right Column) -->
<div class="lg:col-span-5 flex flex-col h-full">
<div class="bg-surface-container-lowest rounded-lg shadow-md border-2 border-surface-variant flex flex-col h-full relative">
<!-- Receipt Top Decoration (simulated zigzag/glass) -->
<div class="h-4 w-full ticket-edge absolute -top-2 left-0 z-10"></div>
<div class="p-8 pt-10 flex-grow flex flex-col relative z-0">
<div class="flex justify-between items-center mb-8 border-b-2 border-surface-variant pb-4 border-dashed">
<h3 class="font-headline-lg text-headline-lg text-text-ink flex items-center gap-3">
<span class="material-symbols-outlined text-primary text-4xl">receipt_long</span>
                                    Última Venda
                                </h3>
<!-- Seal -->
<div class="w-16 h-16 rounded-full bg-mint-success text-on-secondary-fixed-variant flex items-center justify-center font-label-bold text-label-bold text-xs text-center leading-tight shadow-sm border-2 border-white rotate-12 shrink-0">
                                    ⭐<br/>Boa<br/>Venda!
                                </div>
</div>
<!-- Timeline List -->
<div class="flex-grow space-y-6">
<!-- Timeline Item 1 -->
<div class="flex gap-4 items-start relative">
<div class="w-12 h-12 rounded-full bg-error-container text-on-error-container flex items-center justify-center shadow-inner border-2 border-white shrink-0 z-10">
<span class="material-symbols-outlined text-2xl">nutrition</span>
</div>
<div class="bg-surface-container-low rounded-lg p-4 flex-grow border border-surface-variant shadow-sm">
<p class="font-body-lg text-body-lg text-on-surface">
<strong class="text-text-ink">Gustavo</strong> comprou 2 maçãs 🍎
                                        </p>
<p class="font-label-bold text-label-bold text-on-surface-variant mt-1 text-sm">Há 5 minutos</p>
</div>
<!-- Connecting line -->
<div class="absolute left-6 top-12 bottom-[-24px] w-1 bg-surface-variant -z-0"></div>
</div>
<!-- Timeline Item 2 -->
<div class="flex gap-4 items-start relative">
<div class="w-12 h-12 rounded-full bg-primary-container text-on-primary-container flex items-center justify-center shadow-inner border-2 border-white shrink-0 z-10">
<span class="material-symbols-outlined text-2xl">cake</span>
</div>
<div class="bg-surface-container-low rounded-lg p-4 flex-grow border border-surface-variant shadow-sm">
<p class="font-body-lg text-body-lg text-on-surface">
                                            Levou um chocolate 🍫
                                        </p>
<p class="font-label-bold text-label-bold text-on-surface-variant mt-1 text-sm">Há 5 minutos</p>
</div>
</div>
<!-- Empty state or more items could go here -->
<div class="pt-4 flex justify-center">
<div class="px-4 py-2 bg-surface-variant rounded-full font-label-bold text-label-bold text-on-surface-variant text-sm">
                                        Fim do recibo
                                    </div>
</div>
</div>
</div>
<!-- Receipt Bottom Decoration -->
<div class="h-4 w-full ticket-edge absolute -bottom-2 left-0 z-10 rotate-180"></div>
</div>
</div>
</div>
</div>
</main>
</body></html>