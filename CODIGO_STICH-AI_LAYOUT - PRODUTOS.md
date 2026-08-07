<!DOCTYPE html>

<html lang="pt-BR"><head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Mercadinho Feliz - Produtos</title>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com" rel="preconnect"/>
<link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"/>
<link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@400..700&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
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
                      "body-md": [
                              "Quicksand"
                      ],
                      "title-md": [
                              "Quicksand"
                      ],
                      "body-lg": [
                              "Quicksand"
                      ],
                      "display-lg": [
                              "Quicksand"
                      ],
                      "headline-lg": [
                              "Quicksand"
                      ],
                      "label-bold": [
                              "Quicksand"
                      ],
                      "headline-lg-mobile": [
                              "Quicksand"
                      ]
              },
              "fontSize": {
                      "body-md": [
                              "18px",
                              {
                                      "lineHeight": "26px",
                                      "fontWeight": "500"
                              }
                      ],
                      "title-md": [
                              "24px",
                              {
                                      "lineHeight": "32px",
                                      "fontWeight": "600"
                              }
                      ],
                      "body-lg": [
                              "20px",
                              {
                                      "lineHeight": "30px",
                                      "fontWeight": "500"
                              }
                      ],
                      "display-lg": [
                              "48px",
                              {
                                      "lineHeight": "56px",
                                      "letterSpacing": "-0.02em",
                                      "fontWeight": "700"
                              }
                      ],
                      "headline-lg": [
                              "32px",
                              {
                                      "lineHeight": "40px",
                                      "fontWeight": "700"
                              }
                      ],
                      "label-bold": [
                              "16px",
                              {
                                      "lineHeight": "20px",
                                      "letterSpacing": "0.05em",
                                      "fontWeight": "700"
                              }
                      ],
                      "headline-lg-mobile": [
                              "28px",
                              {
                                      "lineHeight": "34px",
                                      "fontWeight": "700"
                              }
                      ]
              }
      },
          },
        }
    </script>
<style>
        body {
            background-color: #f9f9f9;
            background-image: 
                radial-gradient(circle at 20% 30%, rgba(255, 194, 226, 0.4) 0%, transparent 40%),
                radial-gradient(circle at 80% 70%, rgba(188, 233, 255, 0.4) 0%, transparent 40%);
            background-attachment: fixed;
        }

        .toy-shadow {
            box-shadow: 0 8px 0 rgba(101, 56, 83, 0.15), 0 12px 24px rgba(0,0,0,0.05);
        }
        
        .toy-shadow-card {
             box-shadow: 0 6px 0 rgba(226, 226, 226, 1), 0 10px 20px rgba(0,0,0,0.04);
        }

        .toy-button-press:active {
            transform: translateY(4px);
            box-shadow: 0 2px 0 rgba(101, 56, 83, 0.15);
            margin-bottom: 4px;
        }
        
        .toy-card-press:active {
            transform: translateY(4px);
            box-shadow: 0 2px 0 rgba(226, 226, 226, 1);
        }

        .inner-glow {
            box-shadow: inset 0 2px 4px rgba(255,255,255,0.6);
        }
        
        .input-well {
            box-shadow: inset 0 4px 6px rgba(0,0,0,0.05);
        }

        /* Fun Floating Animation for Mascot */
        @keyframes float {
            0% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-10px) rotate(2deg); }
            100% { transform: translateY(0px) rotate(0deg); }
        }
        .animate-float {
            animation: float 3s ease-in-out infinite;
        }
    </style>
</head>
<body class="font-body-md text-on-surface min-h-screen relative overflow-x-hidden">
<!-- TopAppBar -->
<header class="fixed top-0 right-0 left-0 md:left-64 h-20 flex justify-between items-center px-margin-mobile md:px-margin-desktop z-50 bg-magic-lilac dark:bg-on-primary-fixed-variant rounded-b-lg border-b-4 border-primary shadow-lg">
<div class="flex items-center gap-unit">
<!-- Mascot Placeholder Mobile -->
<div class="w-12 h-12 bg-surface-container-lowest rounded-full border-4 border-primary-container flex items-center justify-center shadow-sm overflow-hidden md:hidden animate-float">
<img class="w-full h-full object-cover" data-alt="A cute, 3D rendered mascot character resembling a friendly shopping bag with big expressive eyes and a smiling face. The mascot is designed in a vibrant, toy-like aesthetic with soft, glossy materials. The lighting is bright and cheerful, highlighting the rounded forms against a clean white background. High resolution, colorful, and playful." src="https://lh3.googleusercontent.com/aida-public/AB6AXuD1n96UKUT6ZbnYr-cNuF1bQIXEsLflyWh-mQIOpVLI12UMKNY25FarzcRxem4kmrw3EujANOr0K-w7JwCH9rQ8Dow4mIMugk85XVWrsCzKSa8pVCpECwuo1ktoGqdjnr6Kn028OLZREzcZlRxtNqOS3a77jXS-WfyhbluEF-7u2PF72xN3KtjWXxb5yZ7je51WBRT_g9HKuE95f_Z-qirGqDkWVPO1wUsn1FyJXx3f7aoMVMVfed9J"/>
</div>
<h1 class="font-headline-lg-mobile md:font-headline-lg text-headline-lg-mobile md:text-headline-lg text-on-primary-fixed">Ol\u00e1, \u00cdsis! \ud83c\udf08</h1>
</div>
<div class="flex items-center gap-stack-gap">
<div class="hidden md:flex items-center gap-unit bg-surface-container-lowest py-2 px-4 rounded-full border-2 border-primary-container font-label-bold text-label-bold text-primary inner-glow toy-shadow">
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">stars</span>
<span>N\u00edvel 5 \u2b50\ufe0f</span>
</div>
<div class="hidden md:flex items-center gap-unit bg-surface-container-lowest py-2 px-4 rounded-full border-2 border-primary-container font-label-bold text-label-bold text-primary inner-glow toy-shadow">
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">account_balance_wallet</span>
<span>Cofre: $1,250</span>
</div>
<button class="w-12 h-12 bg-primary-container text-on-primary-container rounded-full flex items-center justify-center border-b-4 border-on-primary-fixed-variant toy-button-press hover:scale-105 transition-transform">
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">notifications</span>
</button>
<button class="w-12 h-12 bg-primary-container text-on-primary-container rounded-full flex items-center justify-center border-b-4 border-on-primary-fixed-variant toy-button-press hover:scale-105 transition-transform hidden md:flex">
<span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">stars</span>
</button>
</div>
</header>
<!-- SideNavBar (Desktop) -->
<nav class="fixed left-0 top-0 h-full flex-col p-4 gap-stack-gap z-40 bg-surface-container-low shadow-[4px_0px_0px_0px_rgba(127,79,107,0.2)] h-full w-64 rounded-r-lg hidden md:flex">
<div class="flex flex-col items-center gap-2 mb-8 mt-4">
<div class="w-24 h-24 bg-surface-container-lowest rounded-full border-4 border-primary-container flex items-center justify-center shadow-md overflow-hidden animate-float">
<img class="w-full h-full object-cover" data-alt="A cute, 3D rendered mascot character resembling a friendly shopping bag with big expressive eyes and a smiling face. The mascot is designed in a vibrant, toy-like aesthetic with soft, glossy materials. The lighting is bright and cheerful, highlighting the rounded forms against a clean white background. High resolution, colorful, and playful." src="https://lh3.googleusercontent.com/aida-public/AB6AXuAEQn3TzgTKDRfy8ijcOJBGOIn35rxaK0D_djD5whKvP7nkH-Cpkre24mK-pVJySSXZPzb-xClndp6P98x0Ae5Xb4uLmq3FLbc6mYCCFsz4K9qt6c7s_2d432KoCUb6Yxf3luHi2_B40giHffARuLdaIywUhInLNymhuEfU50aV_Z4eOCc1N7u2mJ6IbOrB-q7HheIqXolauZeKsa0hExrXWH02Iy7VOjuU8zTbAfLWoLLNJN4mGQC5"/>
</div>
<h2 class="font-title-md text-title-md text-primary text-center">Mercadinho Feliz</h2>
<span class="font-body-md text-body-md text-on-surface-variant">N\u00edvel do Mercado</span>
</div>
<div class="flex flex-col gap-2 flex-grow overflow-y-auto">
<!-- Inactive -->
<a class="flex items-center gap-4 text-on-surface-variant p-4 rounded-xl hover:bg-primary-fixed hover:text-on-primary-fixed-variant transition-all duration-100" href="#">
<span class="material-symbols-outlined text-2xl">home</span>
<span class="font-label-bold text-label-bold">Home</span>
</a>
<!-- Active (Produtos) -->
<a class="flex flex-col items-center justify-center bg-primary-container text-on-primary-container rounded-xl border-b-4 border-on-primary-fixed-variant p-4 transition-all scale-105 active:translate-y-1 active:border-b-0 duration-100" href="#">
<span class="material-symbols-outlined text-3xl mb-1" style="font-variation-settings: 'FILL' 1;">shopping_basket</span>
<span class="font-label-bold text-label-bold">Produtos</span>
</a>
<!-- Inactive -->
<a class="flex items-center gap-4 text-on-surface-variant p-4 rounded-xl hover:bg-primary-fixed hover:text-on-primary-fixed-variant transition-all duration-100" href="#">
<span class="material-symbols-outlined text-2xl">inventory_2</span>
<span class="font-label-bold text-label-bold">Estoque</span>
</a>
<a class="flex items-center gap-4 text-on-surface-variant p-4 rounded-xl hover:bg-primary-fixed hover:text-on-primary-fixed-variant transition-all duration-100" href="#">
<span class="material-symbols-outlined text-2xl">point_of_sale</span>
<span class="font-label-bold text-label-bold">Caixa</span>
</a>
<a class="flex items-center gap-4 text-on-surface-variant p-4 rounded-xl hover:bg-primary-fixed hover:text-on-primary-fixed-variant transition-all duration-100" href="#">
<span class="material-symbols-outlined text-2xl">receipt_long</span>
<span class="font-label-bold text-label-bold">Vendas</span>
</a>
<a class="flex items-center gap-4 text-on-surface-variant p-4 rounded-xl hover:bg-primary-fixed hover:text-on-primary-fixed-variant transition-all duration-100" href="#">
<span class="material-symbols-outlined text-2xl">face_6</span>
<span class="font-label-bold text-label-bold">Clientes</span>
</a>
<a class="flex items-center gap-4 text-on-surface-variant p-4 rounded-xl hover:bg-primary-fixed hover:text-on-primary-fixed-variant transition-all duration-100" href="#">
<span class="material-symbols-outlined text-2xl">analytics</span>
<span class="font-label-bold text-label-bold">Relat\u00f3rios</span>
</a>
<a class="flex items-center gap-4 text-on-surface-variant p-4 rounded-xl hover:bg-primary-fixed hover:text-on-primary-fixed-variant transition-all duration-100" href="#">
<span class="material-symbols-outlined text-2xl">settings</span>
<span class="font-label-bold text-label-bold">Ajustes</span>
</a>
</div>
<button class="mt-auto bg-action-orange text-white font-label-bold text-label-bold py-3 px-4 rounded-xl border-b-4 border-[#cc7c33] toy-button-press inner-glow transition-all">
            Ver Conquistas
        </button>
</nav>
<!-- BottomNavBar (Mobile) -->
<nav class="fixed bottom-0 left-0 right-0 h-20 bg-surface-container-low flex md:hidden justify-around items-center px-2 z-40 rounded-t-lg shadow-[0px_-4px_16px_0px_rgba(0,0,0,0.1)]">
<!-- Active (Produtos) -->
<a class="flex flex-col items-center justify-center text-on-primary-fixed bg-primary-container p-2 rounded-xl -mt-6 border-b-4 border-on-primary-fixed-variant toy-button-press transition-all h-16 w-16" href="#">
<span class="material-symbols-outlined text-2xl" style="font-variation-settings: 'FILL' 1;">shopping_basket</span>
<span class="text-[10px] font-bold mt-1">Prod</span>
</a>
<a class="flex flex-col items-center justify-center text-on-surface-variant p-2 rounded-xl" href="#">
<span class="material-symbols-outlined text-2xl">inventory_2</span>
</a>
<a class="flex flex-col items-center justify-center text-on-surface-variant p-2 rounded-xl" href="#">
<span class="material-symbols-outlined text-2xl">point_of_sale</span>
</a>
<a class="flex flex-col items-center justify-center text-on-surface-variant p-2 rounded-xl" href="#">
<span class="material-symbols-outlined text-2xl">receipt_long</span>
</a>
</nav>
<!-- Main Content Area -->
<main class="pt-28 pb-24 md:pb-8 md:pl-[280px] px-margin-mobile md:px-margin-desktop min-h-screen">
<!-- Header Actions -->
<div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-stack-gap mb-8">
<!-- Search Bar -->
<div class="relative w-full md:w-96">
<div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
<span class="material-symbols-outlined text-primary text-2xl">search</span>
</div>
<input class="w-full pl-12 pr-4 py-4 rounded-xl bg-surface-container-lowest border-2 border-primary-container text-body-lg font-body-lg placeholder:text-on-surface-variant text-on-surface input-well focus:outline-none focus:border-primary transition-colors" placeholder="Procurar produtos..." type="text"/>
</div>
<!-- Add Product Button -->
<button class="w-full md:w-auto flex items-center justify-center gap-2 bg-mint-success text-on-secondary-fixed py-4 px-6 rounded-xl border-b-[6px] border-[#89c2ab] font-label-bold text-label-bold inner-glow toy-button-press transition-transform">
<span class="text-2xl">🎁</span>
<span>Adicionar Novo</span>
</button>
</div>
<!-- Category Chips -->
<div class="flex gap-4 overflow-x-auto pb-4 mb-4 scrollbar-hide -mx-margin-mobile px-margin-mobile md:mx-0 md:px-0">
<button class="flex-shrink-0 bg-primary text-on-primary py-2 px-6 rounded-full font-label-bold text-label-bold border-b-4 border-on-primary-fixed-variant toy-button-press inner-glow">Todos</button>
<button class="flex-shrink-0 bg-secondary-container text-on-secondary-container py-2 px-6 rounded-full font-label-bold text-label-bold border-b-4 border-[#81b2ca] toy-button-press inner-glow">Brinquedos</button>
<button class="flex-shrink-0 bg-tertiary-container text-on-tertiary-container py-2 px-6 rounded-full font-label-bold text-label-bold border-b-4 border-[#b1a76c] toy-button-press inner-glow">Comidas</button>
<button class="flex-shrink-0 bg-error-container text-on-error-container py-2 px-6 rounded-full font-label-bold text-label-bold border-b-4 border-[#d5b0ae] toy-button-press inner-glow">Bebidas</button>
</div>
<!-- Products Grid -->
<div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 md:gap-gutter">
<!-- Product Card 1 -->
<div class="bg-surface-container-lowest rounded-[32px] p-4 border-2 border-[#b1a76c] flex flex-col items-center text-center toy-shadow-card toy-card-press transition-transform cursor-pointer relative group">
<div class="absolute top-3 right-3 w-8 h-8 bg-tertiary-container rounded-full flex items-center justify-center text-on-tertiary-container font-bold shadow-sm">
                    3
                </div>
<div class="text-[64px] mb-2 group-hover:scale-110 transition-transform duration-300">🍎</div>
<h3 class="font-title-md text-title-md text-on-surface mb-1">Maçã</h3>
<div class="bg-tertiary-container text-on-tertiary-container px-3 py-1 rounded-lg font-label-bold text-label-bold mb-3 border-b-2 border-[#b1a76c]">
                    $2.00
                </div>
<div class="w-full flex gap-1 justify-center mt-auto">
<span class="material-symbols-outlined text-mint-success text-sm" style="font-variation-settings: 'FILL' 1;">star</span>
<span class="material-symbols-outlined text-mint-success text-sm" style="font-variation-settings: 'FILL' 1;">star</span>
<span class="material-symbols-outlined text-mint-success text-sm" style="font-variation-settings: 'FILL' 1;">star</span>
<span class="material-symbols-outlined text-surface-variant text-sm" style="font-variation-settings: 'FILL' 1;">star</span>
</div>
</div>
<!-- Product Card 2 -->
<div class="bg-surface-container-lowest rounded-[32px] p-4 border-2 border-[#81b2ca] flex flex-col items-center text-center toy-shadow-card toy-card-press transition-transform cursor-pointer relative group">
<div class="text-[64px] mb-2 group-hover:scale-110 transition-transform duration-300">🧸</div>
<h3 class="font-title-md text-title-md text-on-surface mb-1">Ursinho</h3>
<div class="bg-secondary-container text-on-secondary-container px-3 py-1 rounded-lg font-label-bold text-label-bold mb-3 border-b-2 border-[#81b2ca]">
                    $15.00
                </div>
<div class="w-full flex gap-1 justify-center mt-auto">
<span class="material-symbols-outlined text-mint-success text-sm" style="font-variation-settings: 'FILL' 1;">star</span>
<span class="material-symbols-outlined text-mint-success text-sm" style="font-variation-settings: 'FILL' 1;">star</span>
<span class="material-symbols-outlined text-surface-variant text-sm" style="font-variation-settings: 'FILL' 1;">star</span>
<span class="material-symbols-outlined text-surface-variant text-sm" style="font-variation-settings: 'FILL' 1;">star</span>
</div>
</div>
<!-- Product Card 3 -->
<div class="bg-surface-container-lowest rounded-[32px] p-4 border-2 border-[#d5b0ae] flex flex-col items-center text-center toy-shadow-card toy-card-press transition-transform cursor-pointer relative group">
<div class="absolute top-3 right-3 w-8 h-8 bg-error-container rounded-full flex items-center justify-center text-on-error-container font-bold shadow-sm">
                    8
                </div>
<div class="text-[64px] mb-2 group-hover:scale-110 transition-transform duration-300">🥛</div>
<h3 class="font-title-md text-title-md text-on-surface mb-1">Leite</h3>
<div class="bg-error-container text-on-error-container px-3 py-1 rounded-lg font-label-bold text-label-bold mb-3 border-b-2 border-[#d5b0ae]">
                    $4.50
                </div>
<div class="w-full h-3 bg-surface-variant rounded-full mt-auto overflow-hidden">
<div class="h-full bg-mint-success w-3/4 rounded-full"></div>
</div>
</div>
<!-- Product Card 4 -->
<div class="bg-surface-container-lowest rounded-[32px] p-4 border-2 border-[#81b2ca] flex flex-col items-center text-center toy-shadow-card toy-card-press transition-transform cursor-pointer relative group">
<div class="text-[64px] mb-2 group-hover:scale-110 transition-transform duration-300">🚗</div>
<h3 class="font-title-md text-title-md text-on-surface mb-1">Carrinho</h3>
<div class="bg-secondary-container text-on-secondary-container px-3 py-1 rounded-lg font-label-bold text-label-bold mb-3 border-b-2 border-[#81b2ca]">
                    $8.00
                </div>
<div class="w-full h-3 bg-surface-variant rounded-full mt-auto overflow-hidden">
<div class="h-full bg-mint-success w-1/4 rounded-full"></div>
</div>
</div>
<!-- Product Card 5 -->
<div class="bg-surface-container-lowest rounded-[32px] p-4 border-2 border-[#b1a76c] flex flex-col items-center text-center toy-shadow-card toy-card-press transition-transform cursor-pointer relative group">
<div class="text-[64px] mb-2 group-hover:scale-110 transition-transform duration-300">🍫</div>
<h3 class="font-title-md text-title-md text-on-surface mb-1">Chocolate</h3>
<div class="bg-tertiary-container text-on-tertiary-container px-3 py-1 rounded-lg font-label-bold text-label-bold mb-3 border-b-2 border-[#b1a76c]">
                    $3.00
                </div>
<div class="w-full flex gap-1 justify-center mt-auto">
<span class="material-symbols-outlined text-mint-success text-sm" style="font-variation-settings: 'FILL' 1;">star</span>
<span class="material-symbols-outlined text-surface-variant text-sm" style="font-variation-settings: 'FILL' 1;">star</span>
<span class="material-symbols-outlined text-surface-variant text-sm" style="font-variation-settings: 'FILL' 1;">star</span>
<span class="material-symbols-outlined text-surface-variant text-sm" style="font-variation-settings: 'FILL' 1;">star</span>
</div>
</div>
</div>
</main>
</body></html>