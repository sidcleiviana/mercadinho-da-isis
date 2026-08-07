(function () {
    "use strict";

    var rootId = "mercadinho-effects-root";
    var achievementStore = "mercadinho-achievements";
    var clientMemoryStore = "mercadinho-client-memory";
    var clientArrivalStore = "mercadinho-client-arrivals";
    var audioContext = null;
    var femaleNames = [
        "isis", "alice", "helena", "laura", "valentina", "sofia", "cecilia", "manuela",
        "luna", "liz", "beatriz", "julia", "maria", "heloisa", "clara", "elisa",
        "aurora", "catarina", "melissa", "bianca", "ana", "fernanda"
    ];
    var maleNames = [
        "miguel", "arthur", "theo", "davi", "bernardo", "gabriel", "lucas", "pedro",
        "rafael", "enzo", "samuel", "heitor", "matheus", "henrique", "benjamin", "caio",
        "joaquim", "nicolas", "felipe", "daniel", "carlos", "joao", "gustavo"
    ];
    var characterProfiles = [
        { emoji: "👧", gender: "female", title: "Menina sorridente", mood: "😊", color: "#ffc2e2" },
        { emoji: "👧", gender: "female", title: "Menina de laço", mood: "😍", color: "#ffe4f1" },
        { emoji: "👩", gender: "female", title: "Mamãe alegre", mood: "🥰", color: "#ffd1dc" },
        { emoji: "👵", gender: "female", title: "Vovó simpática", mood: "🥰", color: "#fff0a8" },
        { emoji: "👦", gender: "male", title: "Menino de boné", mood: "😄", color: "#a6e2fe" },
        { emoji: "👦", gender: "male", title: "Menino curioso", mood: "🤔", color: "#b4f2d6" },
        { emoji: "👨", gender: "male", title: "Papai alegre", mood: "😄", color: "#b8e8ff" },
        { emoji: "👴", gender: "male", title: "Vovô gentil", mood: "😊", color: "#e8d5ff" },
        { emoji: "🧒", gender: "any", title: "Criança curiosa", mood: "🤔", color: "#b4f2d6" },
        { emoji: "🧑‍🍳", gender: "any", title: "Cozinheiro", mood: "😋", color: "#ffe0b5" },
        { emoji: "🦸", gender: "any", title: "Super-herói", mood: "🥳", color: "#d5c7ff" },
        { emoji: "🧙", gender: "any", title: "Mago", mood: "😲", color: "#d9c2ff" },
        { emoji: "🧸", gender: "any", title: "Ursinho", mood: "🥰", color: "#f6d7b8" },
        { emoji: "🐼", gender: "any", title: "Panda", mood: "😊", color: "#e5e7eb" },
        { emoji: "🐱", gender: "any", title: "Gatinho", mood: "😺", color: "#ffd6a5" },
        { emoji: "🐰", gender: "any", title: "Coelhinho", mood: "😍", color: "#ffe4f1" },
        { emoji: "🐶", gender: "any", title: "Cachorrinho", mood: "😄", color: "#d8b894" },
        { emoji: "🐸", gender: "any", title: "Sapinho", mood: "🤗", color: "#b4f2d6" }
    ];
    var personalityLines = [
        "Que mercadinho bonito!",
        "Adorei seu caixa!",
        "Seu mercado está muito organizado!",
        "Posso voltar amanhã?",
        "Nossa, que prateleiras caprichadas!",
        "Você foi muito rápido!",
        "Estou escolhendo com calma...",
        "Hoje eu quero uma compra especial!"
    ];

    function getRoot() {
        var root = document.getElementById(rootId);
        if (!root) {
            root = document.createElement("div");
            root.id = rootId;
            root.setAttribute("aria-live", "polite");
            document.body.appendChild(root);
        }
        return root;
    }

    function getAudioContext() {
        if (!audioContext) {
            var Context = window.AudioContext || window.webkitAudioContext;
            if (!Context) {
                return null;
            }
            audioContext = new Context();
        }
        if (audioContext.state === "suspended") {
            audioContext.resume().catch(function () {});
        }
        return audioContext;
    }

    function tone(frequency, duration, type, volume, delay) {
        var ctx = getAudioContext();
        if (!ctx) {
            return;
        }
        var start = ctx.currentTime + (delay || 0);
        var oscillator = ctx.createOscillator();
        var gain = ctx.createGain();

        oscillator.type = type || "sine";
        oscillator.frequency.setValueAtTime(frequency, start);
        gain.gain.setValueAtTime(0.001, start);
        gain.gain.exponentialRampToValueAtTime(volume || 0.12, start + 0.015);
        gain.gain.exponentialRampToValueAtTime(0.001, start + duration);

        oscillator.connect(gain);
        gain.connect(ctx.destination);
        oscillator.start(start);
        oscillator.stop(start + duration + 0.03);
    }

    function sound(name) {
        if (name === "scanner") {
            tone(980, 0.08, "square", 0.07);
        } else if (name === "success") {
            tone(720, 0.08, "sine", 0.08);
            tone(1040, 0.12, "sine", 0.08, 0.08);
        } else if (name === "error") {
            tone(220, 0.14, "sawtooth", 0.06);
            tone(160, 0.18, "sawtooth", 0.05, 0.12);
        } else if (name === "cash") {
            tone(840, 0.08, "triangle", 0.09);
            tone(1280, 0.12, "triangle", 0.08, 0.08);
            tone(1660, 0.16, "triangle", 0.06, 0.18);
        } else if (name === "bell") {
            tone(1180, 0.12, "sine", 0.08);
            tone(860, 0.16, "sine", 0.06, 0.13);
        } else if (name === "fanfare") {
            [660, 880, 990, 1320].forEach(function (note, index) {
                tone(note, 0.11, "triangle", 0.07, index * 0.09);
            });
        } else if (name === "printer") {
            for (var i = 0; i < 10; i += 1) {
                tone(i % 2 ? 310 : 360, 0.025, "square", 0.025, i * 0.035);
            }
        }
    }

    function normalize(text) {
        return (text || "")
            .toLowerCase()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "");
    }

    function makeEl(tag, className, text) {
        var el = document.createElement(tag);
        if (className) {
            el.className = className;
        }
        if (text !== undefined) {
            el.textContent = text;
        }
        return el;
    }

    function toast(message, type) {
        var item = makeEl("div", "mf-toast mf-toast-" + (type || "success"));
        item.textContent = message;
        getRoot().appendChild(item);
        window.setTimeout(function () {
            item.classList.add("mf-leaving");
            window.setTimeout(function () {
                item.remove();
            }, 280);
        }, 2300);
        return item;
    }

    function confetti(count) {
        var box = makeEl("div", "mf-confetti", "");
        var emojis = ["⭐", "✨", "🎉", "💖", "🌈", "🍭"];
        var total = count || 44;
        for (var i = 0; i < total; i += 1) {
            var piece = makeEl("span", "mf-confetti-piece", emojis[i % emojis.length]);
            piece.style.setProperty("--x", Math.round(Math.random() * 100) + "vw");
            piece.style.setProperty("--delay", (Math.random() * 0.35).toFixed(2) + "s");
            piece.style.setProperty("--spin", Math.round(Math.random() * 260 - 130) + "deg");
            box.appendChild(piece);
        }
        getRoot().appendChild(box);
        window.setTimeout(function () {
            box.remove();
        }, 3200);
    }

    function stars(target) {
        var host = target || getRoot();
        for (var i = 0; i < 8; i += 1) {
            var star = makeEl("span", "mf-star", i % 2 ? "✨" : "⭐");
            star.style.setProperty("--left", Math.round(10 + Math.random() * 80) + "%");
            star.style.setProperty("--top", Math.round(10 + Math.random() * 72) + "%");
            host.appendChild(star);
            window.setTimeout(function (el) {
                el.remove();
            }, 1300, star);
        }
    }

    function bounce(target) {
        if (!target) {
            return;
        }
        target.classList.remove("mf-bounce");
        void target.offsetWidth;
        target.classList.add("mf-bounce");
    }

    function shake(target) {
        if (!target) {
            return;
        }
        target.classList.remove("mf-shake");
        void target.offsetWidth;
        target.classList.add("mf-shake");
    }

    function readAchievements() {
        try {
            return JSON.parse(window.localStorage.getItem(achievementStore) || "{}");
        } catch (error) {
            return {};
        }
    }

    function saveAchievements(done) {
        try {
            window.localStorage.setItem(achievementStore, JSON.stringify(done));
        } catch (error) {}
    }

    function achievement(key, label) {
        var done = readAchievements();
        if (done[key]) {
            return;
        }
        done[key] = true;
        saveAchievements(done);
        sound("fanfare");
        var card = makeEl("div", "mf-achievement");
        card.innerHTML = '<span class="mf-achievement-medal">🏅</span><strong>Conquista desbloqueada!</strong><p>' + label + "</p>";
        getRoot().appendChild(card);
        window.setTimeout(function () {
            card.classList.add("mf-leaving");
            window.setTimeout(function () {
                card.remove();
            }, 350);
        }, 3600);
    }

    function celebration(title, subtitle) {
        sound("cash");
        confetti(58);
        var overlay = makeEl("div", "mf-celebration");
        overlay.innerHTML =
            '<div class="mf-celebration-card">' +
            '<div class="mf-celebration-icon">🎉</div>' +
            "<h2>" + title + "</h2>" +
            "<p>" + subtitle + "</p>" +
            '<div class="mf-rating">⭐⭐⭐⭐⭐</div>' +
            "</div>";
        getRoot().appendChild(overlay);
        stars(overlay);
        window.setTimeout(function () {
            overlay.classList.add("mf-leaving");
            window.setTimeout(function () {
                overlay.remove();
            }, 360);
        }, 2200);
    }

    function productEmoji(name) {
        var value = normalize(name);
        if (value.indexOf("maca") >= 0 || value.indexOf("banana") >= 0 || value.indexOf("fruta") >= 0) {
            return "🍎";
        }
        if (value.indexOf("chocolate") >= 0 || value.indexOf("doce") >= 0 || value.indexOf("bala") >= 0) {
            return "🍫";
        }
        if (value.indexOf("leite") >= 0 || value.indexOf("iogurte") >= 0) {
            return "🥛";
        }
        if (value.indexOf("arroz") >= 0 || value.indexOf("feijao") >= 0) {
            return "🛒";
        }
        return "✨";
    }

    function hashText(text) {
        var hash = 0;
        var value = String(text || "mercadinho");
        for (var i = 0; i < value.length; i += 1) {
            hash = ((hash << 5) - hash) + value.charCodeAt(i);
            hash |= 0;
        }
        return Math.abs(hash);
    }

    function readJsonStore(key) {
        try {
            return JSON.parse(window.localStorage.getItem(key) || "{}");
        } catch (error) {
            return {};
        }
    }

    function saveJsonStore(key, value) {
        try {
            window.localStorage.setItem(key, JSON.stringify(value));
        } catch (error) {}
    }

    function clientKey(name) {
        return normalize(name || "cliente").replace(/\s+/g, "-");
    }

    function genderForName(name) {
        var key = clientKey(name);
        if (femaleNames.indexOf(key) >= 0) {
            return "female";
        }
        if (maleNames.indexOf(key) >= 0) {
            return "male";
        }
        return "any";
    }

    function profileForClient(name, id) {
        var seed = hashText((name || "") + ":" + (id || ""));
        var gender = genderForName(name);
        var compatibleProfiles = characterProfiles.filter(function (profile) {
            if (gender === "any") {
                return true;
            }
            if (seed % 6 === 0) {
                return profile.gender === gender || profile.gender === "any";
            }
            return profile.gender === gender;
        });
        var profiles = compatibleProfiles.length ? compatibleProfiles : characterProfiles;
        var profile = profiles[seed % profiles.length];
        var shirtColors = ["#ffc2e2", "#a6e2fe", "#fff0a8", "#b4f2d6", "#e8d5ff", "#ffd6a5", "#ffb3c7", "#c7f9cc"];
        var hairColors = ["#6b3f2f", "#2f241f", "#9a6a3a", "#f2c078", "#5b4b8a", "#7f4f6b"];
        var accessories = ["🎀", "🧢", "🕶️", "🎒", "⭐", "🌈", ""];
        var accessory = accessories[(seed + 3) % accessories.length];
        if (gender === "female" && seed % 3 === 0) {
            accessory = "🎀";
        }
        if (gender === "male" && seed % 3 === 0) {
            accessory = "🧢";
        }
        return {
            emoji: profile.emoji,
            title: profile.title,
            mood: profile.mood,
            color: profile.color,
            shirt: shirtColors[seed % shirtColors.length],
            accent: shirtColors[(seed + 2) % shirtColors.length],
            hair: hairColors[seed % hairColors.length],
            accessory: accessory,
            personality: personalityLines[seed % personalityLines.length]
        };
    }

    function getClientMemory(name) {
        var memory = readJsonStore(clientMemoryStore);
        return memory[clientKey(name)] || { visits: 0, lastProduct: "", lastSeen: "" };
    }

    function rememberClient(name, product) {
        var memory = readJsonStore(clientMemoryStore);
        var key = clientKey(name);
        var current = memory[key] || { visits: 0, lastProduct: "", lastSeen: "" };
        current.visits += 1;
        current.lastSeen = new Date().toISOString();
        if (product) {
            current.lastProduct = product;
        }
        memory[key] = current;
        saveJsonStore(clientMemoryStore, memory);
        return current;
    }

    function clientAvatar(name, id, status, size) {
        var profile = profileForClient(name, id);
        var mood = profile.mood;
        if (status === "em_atendimento") {
            mood = "😊";
        } else if (status === "finalizado") {
            mood = "🥳";
        } else if (status === "desistiu") {
            mood = "👋";
        }
        return (
            '<span class="mf-client-avatar mf-client-avatar-' + (size || "normal") + '" style="--avatar-bg:' + profile.color + '; --avatar-shirt:' + profile.shirt + '; --avatar-accent:' + profile.accent + '">' +
            '<span class="mf-client-shadow"></span>' +
            '<span class="mf-client-body">' +
            '<span class="mf-client-hair" style="--avatar-hair:' + profile.hair + '" aria-hidden="true"></span>' +
            '<span class="mf-client-accessory" aria-hidden="true">' + profile.accessory + '</span>' +
            '<span class="mf-client-emoji">' + profile.emoji + '</span>' +
            '<span class="mf-client-blink" aria-hidden="true"></span>' +
            '<span class="mf-client-smile" aria-hidden="true">' + mood + '</span>' +
            '</span>' +
            '<span class="mf-client-shirt"></span>' +
            '</span>'
        );
    }

    function waitBubbleText(name, status, enteredAt) {
        var memory = getClientMemory(name);
        var profile = profileForClient(name, name);
        if (status === "em_atendimento") {
            return "😊 Estou escolhendo meus produtos!";
        }
        if (memory.visits > 0 && memory.lastProduct) {
            return "😊 Oi! Voltei! Gostei de " + memory.lastProduct + " da última vez!";
        }
        if (memory.visits > 0) {
            return "🐼 Lembra de mim? Vim fazer compras de novo!";
        }
        if (enteredAt) {
            var entered = new Date(enteredAt);
            if (!Number.isNaN(entered.getTime())) {
                var minutes = Math.max(0, Math.floor((Date.now() - entered.getTime()) / 60000));
                if (minutes >= 2) {
                    return "😴 Estou esperando faz " + minutes + " minutinhos...";
                }
            }
        }
        return profile.mood + " " + profile.personality;
    }

    function extractClientName(text) {
        var clean = String(text || "")
            .replace(/^[^\p{L}\p{N}]+/u, "")
            .trim();
        var match = clean.match(/^(.+?)\s+(acabou|est[aá]|veio|entrou|quer|foi|esperou|decidiu|saiu|terminou|adorou|levou|finalizou|comprou)/i);
        return match ? match[1].trim() : "";
    }

    function updateNavBadge(count) {
        var nav = document.querySelector("[data-nav-atendimento]");
        if (!nav) {
            return;
        }
        var badge = nav.querySelector(".mf-nav-badge");
        if (!badge) {
            badge = makeEl("span", "mf-nav-badge", "");
            nav.appendChild(badge);
        }
        if (count > 0) {
            badge.textContent = count;
            nav.classList.add("mf-nav-attention");
            window.setTimeout(function () {
                nav.classList.remove("mf-nav-attention");
            }, 5200);
        } else {
            badge.remove();
            nav.classList.remove("mf-nav-attention");
        }
    }

    function notifyNewClient(card, name, id) {
        var arrivals = readJsonStore(clientArrivalStore);
        var key = "atendimento-" + id;
        if (arrivals[key]) {
            return;
        }
        arrivals[key] = new Date().toISOString();
        saveJsonStore(clientArrivalStore, arrivals);

        var profile = profileForClient(name, id);
        var memory = getClientMemory(name);
        var message = memory.visits > 0 && memory.lastProduct
            ? profile.mood + " " + name + " voltou! Gostou de " + memory.lastProduct + " da última vez."
            : profile.mood + " " + name + " quer fazer compras!";

        sound("bell");
        toast("🔔 Novo cliente chegou! " + message, "success");
        card.classList.add("mf-client-walk-in");
        updateNavBadge(document.querySelectorAll(".client-card-waiting").length);
    }

    function decorateClientCards() {
        var cards = document.querySelectorAll("[data-client-card]");
        if (!cards.length) {
            updateNavBadge(0);
            return;
        }
        cards.forEach(function (card) {
            var name = card.dataset.clientName || "Cliente";
            var id = card.dataset.clientId || name;
            var status = card.dataset.clientStatus || "";
            var slot = card.querySelector(".client-avatar-slot");
            if (slot && !slot.dataset.ready) {
                slot.innerHTML = clientAvatar(name, id, status, "normal");
                slot.dataset.ready = "true";
            }
            var bubble = card.querySelector(".client-wait-bubble");
            if (bubble) {
                bubble.textContent = waitBubbleText(name, status, card.dataset.clientEntered);
            }
            card.dataset.characterReady = "true";
            if (card.classList.contains("client-card-waiting")) {
                notifyNewClient(card, name, id);
            }
        });

        var miniLine = document.querySelector(".client-mini-line");
        if (miniLine) {
            miniLine.innerHTML = "";
            cards.forEach(function (card) {
                if (!card.classList.contains("client-card-waiting")) {
                    return;
                }
                var mini = makeEl("span", "mf-client-mini", "");
                mini.innerHTML = clientAvatar(card.dataset.clientName, card.dataset.clientId, card.dataset.clientStatus, "mini");
                miniLine.appendChild(mini);
            });
        }
        updateNavBadge(document.querySelectorAll(".client-card-waiting").length);
    }

    function friendlyChatText(text, origin) {
        var value = normalize(text);
        var productMatch = text.match(/de\s+(.+?)\.?$/i);
        var product = productMatch ? productMatch[1].replace(/\.$/, "") : "";
        if (origin === "sistema" && value.indexOf("cliente pede") >= 0 && product) {
            return "Oi! Hoje quero comprar " + productEmoji(product) + " " + product + "!";
        }
        if (origin === "sistema" && value.indexOf("produto adicionado") >= 0) {
            return "Que legal! Esse produto entrou na minha comprinha.";
        }
        if (origin === "sistema" && value.indexOf("atendimento encerrado") >= 0) {
            return "Tudo bem, eu volto outro dia.";
        }
        if (origin === "operadora" && value.indexOf("sim") >= 0) {
            return "Tenho sim! Vou colocar na compra.";
        }
        if (origin === "operadora" && value.indexOf("nao") >= 0) {
            return "Hoje não temos esse produto.";
        }
        if (origin === "operadora" && value.indexOf("verificar outros") >= 0) {
            return "Vamos olhar outros produtos bonitos.";
        }
        if (origin === "operadora" && value.indexOf("finalizar") >= 0) {
            return "Vamos finalizar a compra!";
        }
        return text;
    }

    function decorateConversation() {
        var area = document.querySelector("[data-conversation-area]");
        if (!area) {
            return;
        }
        var name = area.dataset.clientName || "Cliente";
        var id = area.dataset.clientId || name;
        var status = area.dataset.clientStatus || "em_atendimento";
        var headSlot = area.querySelector(".conversation-client-head .client-avatar-slot");
        if (headSlot && !headSlot.dataset.ready) {
            headSlot.innerHTML = clientAvatar(name, id, status, "normal");
            headSlot.dataset.ready = "true";
        }
        area.querySelectorAll("[data-chat-message]").forEach(function (message, index) {
            if (message.dataset.ready) {
                return;
            }
            var origin = message.dataset.chatOrigin || "";
            var textSpan = message.querySelector("span");
            var original = message.dataset.chatText || (textSpan ? textSpan.textContent : "");
            var face = origin === "operadora" ? "🧒" : profileForClient(name, id).mood;
            var typing = makeEl("span", "mf-typing", "💬 ...");
            typing.style.setProperty("--delay", (index * 120) + "ms");
            message.parentNode.insertBefore(typing, message);
            message.classList.add("mf-chat-bubble", origin === "operadora" ? "mf-chat-operator" : "mf-chat-client");
            message.style.setProperty("--delay", (index * 120 + 180) + "ms");
            message.insertBefore(makeEl("span", "mf-chat-face", face), message.firstChild);
            if (textSpan) {
                textSpan.textContent = friendlyChatText(original, origin);
            }
            message.dataset.ready = "true";
        });
        document.querySelectorAll("[data-product-request]").forEach(function (item) {
            if (item.dataset.ready) {
                return;
            }
            var nameValue = item.dataset.productRequest || item.textContent.trim();
            item.insertAdjacentHTML("afterbegin", '<span class="mf-product-illustration">' + productEmoji(nameValue) + "</span>");
            item.dataset.ready = "true";
        });
    }

    function handleClientEvents() {
        var seen = readJsonStore("mercadinho-client-events");
        document.querySelectorAll("[data-client-event]").forEach(function (eventItem) {
            var text = eventItem.dataset.eventMessage || eventItem.textContent || "";
            var key = normalize(text);
            if (seen[key]) {
                return;
            }
            seen[key] = true;
            var value = normalize(text);
            var name = extractClientName(text);
            if ((value.indexOf("entrou") >= 0 || value.indexOf("acabou de chegar") >= 0 || value.indexOf("acabou de entrar") >= 0) && name) {
                sound("bell");
            }
            if ((value.indexOf("comprou") >= 0 || value.indexOf("finalizou uma compra") >= 0 || value.indexOf("saiu feliz") >= 0 || value.indexOf("levou") >= 0) && name) {
                var productHint = "produtos";
                rememberClient(name, productHint);
                toast("🥳 " + name + " comemorou a compra!", "success");
                confetti(24);
            }
            if ((value.indexOf("foi atendido") >= 0 || value.indexOf("desistiu") >= 0 || value.indexOf("foi embora") >= 0 || value.indexOf("voltou outro dia") >= 0) && name) {
                rememberClient(name);
            }
        });
        saveJsonStore("mercadinho-client-events", seen);
    }

    function lastProductName() {
        var rows = document.querySelectorAll(".sale-items-panel tbody tr");
        if (!rows.length) {
            return "Produto";
        }
        var firstCell = rows[rows.length - 1].querySelector("td");
        return firstCell ? firstCell.textContent.trim() : "Produto";
    }

    function parseMoney(value) {
        var clean = String(value || "0").replace(/[^\d,.-]/g, "").replace(/\./g, "").replace(",", ".");
        var parsed = Number.parseFloat(clean);
        return Number.isFinite(parsed) ? parsed : 0;
    }

    function closeModal(modal) {
        modal.classList.add("mf-leaving");
        window.setTimeout(function () {
            modal.remove();
        }, 280);
    }

    function submitAfterPayment(form) {
        form.dataset.effectsBypass = "true";
        form.submit();
    }

    function paymentSuccess(modal, form, title, subtitle, total) {
        var body = modal.querySelector(".mf-payment-body");
        body.innerHTML =
            '<div class="mf-approved">✔</div>' +
            "<h3>" + title + "</h3>" +
            "<p>" + subtitle + "</p>";
        sound("cash");
        confetti(60);
        stars(modal);
        if (total >= 50) {
            toast("🎉 UAU! Essa foi uma compra enorme! ⭐ +50 moedas", "success");
        }
        window.setTimeout(function () {
            closeModal(modal);
            submitAfterPayment(form);
        }, 1500);
    }

    function pixFlow(modal, form, total) {
        var body = modal.querySelector(".mf-payment-body");
        var seconds = 15;
        body.innerHTML =
            '<div class="mf-pay-icon">📱</div>' +
            "<h3>Abra a câmera do seu celular e leia o QR Code.</h3>" +
            '<div class="mf-qr" aria-label="QR Code de brincadeira"></div>' +
            '<strong class="mf-countdown">' + seconds + "...</strong>";
        var countdown = body.querySelector(".mf-countdown");
        var timer = window.setInterval(function () {
            seconds -= 1;
            countdown.textContent = seconds + "...";
            if (seconds <= 0) {
                window.clearInterval(timer);
                paymentSuccess(modal, form, "Pagamento recebido!", "Obrigado pela compra!", total);
            }
        }, 1000);
    }

    function cardFlow(modal, form, total) {
        var body = modal.querySelector(".mf-payment-body");
        body.innerHTML =
            '<div class="mf-card-machine">' +
            '<span class="mf-card-emoji">💳</span>' +
            '<span class="mf-card-line"></span>' +
            '<span class="mf-machine">▣</span>' +
            "</div>" +
            "<h3>Passando o cartão...</h3>";
        window.setTimeout(function () {
            sound("scanner");
            window.setTimeout(function () {
                sound("scanner");
            }, 280);
            paymentSuccess(modal, form, "Pagamento aprovado!", "Cliente feliz, compra pronta.", total);
        }, 7000);
    }

    function cashFlow(modal, form, total) {
        var body = modal.querySelector(".mf-payment-body");
        body.innerHTML =
            '<div class="mf-money-rain"><span>💵</span><span>💵</span><span>💵</span><span>💵</span><strong>💰</strong></div>' +
            "<h3>Recebendo o dinheiro...</h3>";
        window.setTimeout(function () {
            paymentSuccess(modal, form, "Pagamento recebido.", "Obrigado!", total);
        }, 1200);
    }

    function openPaymentModal(form) {
        var total = parseMoney(form.dataset.saleTotal);
        var modal = makeEl("div", "mf-payment-overlay");
        modal.innerHTML =
            '<section class="mf-payment-card" role="dialog" aria-modal="true" aria-label="Escolher pagamento">' +
            '<button class="mf-payment-close" type="button" aria-label="Fechar">×</button>' +
            '<div class="mf-payment-body">' +
            '<div class="mf-pay-icon">🎉</div>' +
            "<h2>Como o cliente vai pagar?</h2>" +
            '<div class="mf-payment-options">' +
            '<button type="button" data-pay="cash"><span>💵</span>Dinheiro</button>' +
            '<button type="button" data-pay="card"><span>💳</span>Cartão</button>' +
            '<button type="button" data-pay="pix"><span>📱</span>PIX</button>' +
            "</div>" +
            "</div>" +
            "</section>";
        getRoot().appendChild(modal);
        modal.querySelector(".mf-payment-close").addEventListener("click", function () {
            closeModal(modal);
        });
        modal.querySelector('[data-pay="cash"]').addEventListener("click", function () {
            cashFlow(modal, form, total);
        });
        modal.querySelector('[data-pay="card"]').addEventListener("click", function () {
            cardFlow(modal, form, total);
        });
        modal.querySelector('[data-pay="pix"]').addEventListener("click", function () {
            pixFlow(modal, form, total);
        });
    }

    function wirePaymentForms() {
        document.querySelectorAll("form[data-payment-form]").forEach(function (form) {
            form.addEventListener("submit", function (event) {
                if (form.dataset.effectsBypass === "true") {
                    return;
                }
                event.preventDefault();
                openPaymentModal(form);
            });
        });
    }

    function handleMessages() {
        document.querySelectorAll(".message").forEach(function (message) {
            var text = message.textContent.trim();
            var value = normalize(text);
            if (message.classList.contains("message-error")) {
                sound("error");
                toast("⚠️ Ops! " + text, "error");
                shake(document.querySelector(".barcode-panel") || message);
                return;
            }

            if (!message.classList.contains("message-success")) {
                return;
            }

            if (value.indexOf("produto adicionado") >= 0) {
                var productName = lastProductName();
                var emoji = productEmoji(productName);
                sound("scanner");
                window.setTimeout(function () {
                    sound("success");
                }, 110);
                toast(emoji + " " + productName + " adicionado! ✨ +1 produto", "success");
                bounce(document.querySelector(".sale-items-panel tbody tr:last-child") || document.querySelector(".sale-items-panel"));
            } else if (value.indexOf("venda concluida") >= 0) {
                achievement("primeira-venda", "🥇 Primeira venda");
                celebration("Compra Finalizada!", "Cliente muito feliz! 💰 Caixa atualizado");
            } else if (value.indexOf("expediente aberto") >= 0 || value.indexOf("expediente iniciado") >= 0) {
                sound("fanfare");
                toast("🏪 Mercado aberto! Boa brincadeira!", "success");
                achievement("mercado-aberto", "🏪 Mercado aberto");
            } else if (value.indexOf("expediente fechado") >= 0 || value.indexOf("expediente encerrado") >= 0) {
                sound("success");
                toast("🌙 Mercado fechado. Até a próxima venda!", "success");
            } else if (value.indexOf("atendimento") >= 0 || value.indexOf("cliente") >= 0) {
                sound("bell");
                toast("😊 Cliente feliz! Continue assim!", "success");
            } else {
                sound("success");
                toast("🌈 Muito bem!", "success");
            }
        });
    }

    function addGlobalInteractions() {
        document.addEventListener("pointerdown", function () {
            getAudioContext();
        }, { once: true });
        document.addEventListener("keydown", function () {
            getAudioContext();
        }, { once: true });

        document.querySelectorAll(".button-primary").forEach(function (button) {
            var text = normalize(button.textContent);
            if (text.indexOf("iniciar expediente") >= 0 || text.indexOf("abrir mercado") >= 0) {
                button.classList.add("mf-market-open-button");
            }
        });
    }

    function init() {
        getRoot();
        addGlobalInteractions();
        decorateClientCards();
        decorateConversation();
        handleClientEvents();
        wirePaymentForms();
        handleMessages();
    }

    window.MercadinhoEffects = {
        achievement: achievement,
        bounce: bounce,
        celebration: celebration,
        confetti: confetti,
        decorateClientCards: decorateClientCards,
        shake: shake,
        sound: sound,
        stars: stars,
        toast: toast
    };

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
}());
