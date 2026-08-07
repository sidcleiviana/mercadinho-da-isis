(function () {
    "use strict";

    var script = document.currentScript;
    var spritePath = script ? script.dataset.sprite : "/static/img/mercadinho-feliz.svg";

    function icon(name, className, title) {
        var label = title ? '<title>' + title + "</title>" : "";
        return (
            '<svg class="mf-svg ' + (className || "") + '" aria-hidden="' + (title ? "false" : "true") + '" focusable="false">' +
            label +
            '<use href="' + spritePath + "#" + name + '"></use>' +
            "</svg>"
        );
    }

    function normalize(text) {
        return String(text || "")
            .toLowerCase()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "");
    }

    function productIconName(name) {
        var value = normalize(name);
        if (value.indexOf("maca") >= 0 || value.indexOf("fruta") >= 0) {
            return "apple";
        }
        if (value.indexOf("banana") >= 0) {
            return "banana";
        }
        if (value.indexOf("leite") >= 0 || value.indexOf("iogurte") >= 0) {
            return "milk";
        }
        if (value.indexOf("chocolate") >= 0 || value.indexOf("doce") >= 0 || value.indexOf("bala") >= 0) {
            return "chocolate";
        }
        if (value.indexOf("refrigerante") >= 0 || value.indexOf("refri") >= 0) {
            return "soda";
        }
        if (value.indexOf("biscoito") >= 0 || value.indexOf("bolacha") >= 0) {
            return "cookie";
        }
        if (value.indexOf("suco") >= 0) {
            return "juice";
        }
        if (value.indexOf("carrinho") >= 0 || value.indexOf("carro") >= 0) {
            return "toy-car";
        }
        if (value.indexOf("bola") >= 0) {
            return "ball";
        }
        if (value.indexOf("boneca") >= 0) {
            return "doll";
        }
        if (value.indexOf("urso") >= 0 || value.indexOf("ursinho") >= 0) {
            return "teddy";
        }
        if (value.indexOf("bloco") >= 0) {
            return "blocks";
        }
        if (value.indexOf("quebra") >= 0 || value.indexOf("puzzle") >= 0) {
            return "puzzle";
        }
        return "basket";
    }

    function expressionPath(expression) {
        if (expression === "surprised") {
            return '<circle cx="76" cy="68" r="3.6" fill="#7f4f6b"/><circle cx="100" cy="68" r="3.6" fill="#7f4f6b"/><ellipse cx="88" cy="84" rx="6" ry="7" fill="#7f4f6b"/>';
        }
        if (expression === "thinking") {
            return '<circle cx="76" cy="68" r="3.2" fill="#7f4f6b"/><circle cx="100" cy="68" r="3.2" fill="#7f4f6b"/><path d="M79 84c6-4 12-4 18 0" fill="none" stroke="#7f4f6b" stroke-width="4" stroke-linecap="round"/><circle cx="111" cy="54" r="4" fill="#fff0a8"/><circle cx="119" cy="46" r="3" fill="#fff0a8"/>';
        }
        if (expression === "celebrating") {
            return '<path d="M73 67c5 4 10 4 15 0M88 67c5 4 10 4 15 0" fill="none" stroke="#7f4f6b" stroke-width="4" stroke-linecap="round"/><path d="M78 85c7 8 13 8 20 0" fill="none" stroke="#7f4f6b" stroke-width="5" stroke-linecap="round"/>';
        }
        if (expression === "waiting") {
            return '<path d="M72 68h9M96 68h9" fill="none" stroke="#7f4f6b" stroke-width="4" stroke-linecap="round"/><path d="M80 84c5 3 11 3 16 0" fill="none" stroke="#7f4f6b" stroke-width="4" stroke-linecap="round"/>';
        }
        if (expression === "waving") {
            return '<circle cx="76" cy="68" r="3.2" fill="#7f4f6b"/><circle cx="100" cy="68" r="3.2" fill="#7f4f6b"/><path d="M78 84c7 6 13 6 20 0" fill="none" stroke="#7f4f6b" stroke-width="4" stroke-linecap="round"/>';
        }
        if (expression === "loved") {
            return '<path d="M70 67c0-4 5-5 7-1 2-4 7-3 7 1 0 5-7 9-7 9s-7-4-7-9zM93 67c0-4 5-5 7-1 2-4 7-3 7 1 0 5-7 9-7 9s-7-4-7-9z" fill="#ff8aa7"/><path d="M78 86c7 6 13 6 20 0" fill="none" stroke="#7f4f6b" stroke-width="4" stroke-linecap="round"/>';
        }
        return '<circle cx="76" cy="68" r="3.2" fill="#7f4f6b"/><circle cx="100" cy="68" r="3.2" fill="#7f4f6b"/><path d="M78 83c7 7 13 7 20 0" fill="none" stroke="#7f4f6b" stroke-width="4" stroke-linecap="round"/>';
    }

    function accessoryShape(accessory) {
        if (accessory === "bow") {
            return '<path d="M55 44c-13-7-20 4-11 11 6 4 11-2 11-11zm0 0c13-7 20 4 11 11-6 4-11-2-11-11z" fill="#ffc2e2" stroke="#7f4f6b" stroke-width="3" stroke-linejoin="round"/>';
        }
        if (accessory === "cap") {
            return '<path d="M57 48c12-15 47-14 58 2-15-6-41-6-58-2z" fill="#a6e2fe" stroke="#7f4f6b" stroke-width="4" stroke-linejoin="round"/><path d="M103 47c12-1 21 2 26 8" fill="none" stroke="#7f4f6b" stroke-width="4" stroke-linecap="round"/>';
        }
        if (accessory === "glasses") {
            return '<path d="M67 70h17m8 0h17m-25 0c3-3 5-3 8 0" fill="none" stroke="#7f4f6b" stroke-width="4" stroke-linecap="round"/><circle cx="76" cy="70" r="8" fill="none" stroke="#7f4f6b" stroke-width="4"/><circle cx="100" cy="70" r="8" fill="none" stroke="#7f4f6b" stroke-width="4"/>';
        }
        if (accessory === "bag") {
            return '<path d="M119 108h20l4 28h-28z" fill="#fff0a8" stroke="#7f4f6b" stroke-width="4" stroke-linejoin="round"/><path d="M124 108c0-8 10-8 10 0" fill="none" stroke="#7f4f6b" stroke-width="3" stroke-linecap="round"/>';
        }
        return "";
    }

    function character(options) {
        var data = options || {};
        var skin = data.skin || "#ffd6a5";
        var hair = data.hair || "#6b3f2f";
        var shirt = data.shirt || "#ffc2e2";
        var accent = data.accent || "#a6e2fe";
        var expression = data.expression || "happy";
        var accessory = data.accessory || "";
        var age = data.age || "child";
        var hairPath = age === "grand"
            ? '<path d="M55 63c4-28 62-28 66 0-16-12-50-12-66 0z" fill="#f4f1ea" stroke="#7f4f6b" stroke-width="4" stroke-linejoin="round"/>'
            : '<path d="M52 62c5-33 68-33 73 0-19-15-53-15-73 0z" fill="' + hair + '" stroke="#7f4f6b" stroke-width="4" stroke-linejoin="round"/>';
        if (age === "baby") {
            hairPath = '<path d="M79 47c7-9 18-4 16 6" fill="none" stroke="' + hair + '" stroke-width="5" stroke-linecap="round"/>';
        }
        if (age === "teen") {
            hairPath = '<path d="M48 63c7-34 77-31 73 3-17-17-42-14-73-3z" fill="' + hair + '" stroke="#7f4f6b" stroke-width="4" stroke-linejoin="round"/>';
        }
        return (
            '<svg class="mf-character-svg" viewBox="0 0 176 176" aria-hidden="true" focusable="false">' +
            '<ellipse cx="88" cy="154" rx="52" ry="10" fill="rgba(127,79,107,.16)"/>' +
            '<path d="M49 150c5-38 73-38 78 0z" fill="' + shirt + '" stroke="#7f4f6b" stroke-width="5" stroke-linejoin="round"/>' +
            '<path d="M66 121l-22 23M110 121l22 23" fill="none" stroke="#7f4f6b" stroke-width="7" stroke-linecap="round"/>' +
            '<circle cx="88" cy="74" r="40" fill="' + skin + '" stroke="#7f4f6b" stroke-width="5"/>' +
            hairPath +
            '<path d="M65 129c12 9 34 9 46 0" fill="none" stroke="' + accent + '" stroke-width="7" stroke-linecap="round"/>' +
            expressionPath(expression) +
            accessoryShape(accessory) +
            "</svg>"
        );
    }

    window.MercadinhoIllustrations = {
        character: character,
        icon: icon,
        productIconName: productIconName,
        spritePath: spritePath
    };
}());
