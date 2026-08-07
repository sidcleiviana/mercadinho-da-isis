(function () {
    "use strict";

    var rootId = "mercadinho-effects-root";
    var achievementStore = "mercadinho-achievements";
    var audioContext = null;

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
        wirePaymentForms();
        handleMessages();
    }

    window.MercadinhoEffects = {
        achievement: achievement,
        bounce: bounce,
        celebration: celebration,
        confetti: confetti,
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
