"""
Gardio Client-Side JavaScript (Turbo Mode)
"""

JS_LOGIC = """
window.js_logic = {
    transform: (text, mode) => {
        if (!text) return "";
        switch(mode) {
            case "Reverse": return text.split("").reverse().join("");
            case "UPPERCASE": return text.toUpperCase();
            case "lowercase": return text.toLowerCase();
            case "Title Case": return text.toLowerCase().split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
            case "Sentence Case": return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase();
            case "No Spaces": return text.replace(/\\s+/g, '');
            case "No Punctuation": return text.replace(/[^\\w\\s]|_/g, "");
            case "Shuffle Words": return text.split(' ').sort(() => Math.random() - 0.5).join(' ');
            default: return text;
        }
    },
    
    wordCount: (text) => {
        if (!text) return ["0", "0", "", "0"];
        const words = text.trim().split(/\\s+/);
        const total = words.length;
        const unique = new Set(words).size;
        const longest = words.reduce((a, b) => a.length > b.length ? a : b, "");
        const avg = total ? (words.join("").length / total).toFixed(1) : "0";
        return [String(total), String(unique), longest, String(avg)];
    },
    
    trim: (text) => {
        if (!text) return "";
        return text.split("\\n").map(l => l.trim()).filter(l => l).join("\\n");
    },
    
    stringOps: (text, op) => {
        if (!text) return "";
        switch(op) {
            case "Length": return String(text.length);
            case "Split (comma)": return JSON.stringify(text.split(","));
            case "Split (space)": return JSON.stringify(text.split(" "));
            case "Join (-)": return text.split(" ").join("-");
            case "Strip": return text.trim();
            case "Is Alpha": return String(/^[a-zA-Z]+$/.test(text));
            case "Is Digit": return String(/^\\d+$/.test(text));
            case "Is Alnum": return String(/^[a-zA-Z0-9]+$/.test(text));
            default: return text;
        }
    }
}
"""
