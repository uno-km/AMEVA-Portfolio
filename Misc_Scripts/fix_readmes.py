import os
import re
import glob

def tex_to_text(tex):
    special_maps = {
        r"L_{e2e} = TTFT + \frac{N}{TPS}": "L_e2e = TTFT + (N / TPS)",
        r"\eta = \frac{T}{E}": "η = T / E",
        r"S(t) = \{ f \in \text{Files} \mid \Delta size(f, t) = 0 \;\land\; \Delta mtime(f, t) = 0 \}": "S(t) = { f in Files | Δsize(f, t) = 0 AND Δmtime(f, t) = 0 }",
        r"f_{PAC}(zip) = \begin{cases} SSH(zip), & \text{if SSH is Available} \\ API(zip), & \text{elif API is Available} \\ Telegram(zip), & \text{otherwise (to MIA Bunker)} \end{cases}": "f_PAC(zip) = SSH(zip) (if SSH is Available) / API(zip) (elif API is Available) / Telegram(zip) (otherwise to MIA Bunker)",
        r"S_a^{(t)} = \left[ A_a^{(t)}, O_a^{(t)}, P_a^{(t)} \right] \in \mathbb{R}^8": "S_a(t) = [ A_a(t), O_a(t), P_a(t) ] in R^8",
        r"E_{a \to b}^{(t)} = E_{a \to b}^{(t-1)} + \rho \cdot \Delta E_{event}": "E_ab(t) = E_ab(t-1) + ρ * ΔE_event",
        r"E_{anger} = \sqrt{\sum_{i=1}^{N} A_{target, i}^2}": "E_anger = sqrt( sum( A_target,i^2 ) )",
        r"E_a^{(t)} = f_{obs}\left( H^{(t)} \right)": "E_a(t) = f_obs( H(t) )",
        r"S_a^{(t)} = f_{trans}\left( S_a^{(t-1)}, E_a^{(t)}, W_{a \to \bullet}^{(t-1)} \right)": "S_a(t) = f_trans( S_a(t-1), E_a(t), W_a->*(t-1) )",
        r"W_{a \to b}^{(t)} = (1 - \rho) W_{a \to b}^{(t-1)} + \rho \Delta W(E_a^{(t)})": "W_ab(t) = (1 - ρ) * W_ab(t-1) + ρ * ΔW(E_a(t))",
        r"P\left( \alpha_a^{(t)} = k \mid S_a^{(t)} \right) = \text{softmax}\left( \mathbf{W}_{policy} \cdot S_a^{(t)} \right)_k": "P( α_a(t) = k | S_a(t) ) = softmax( W_policy * S_a(t) )_k",
        r"C_a^{(t)} = g_{gen}\left( \text{Prompt}\left( S_a^{(t)}, \alpha_a^{(t)} \right), H^{(t)} \right)": "C_a(t) = g_gen( Prompt( S_a(t), α_a(t) ), H(t) )",
        r"H^{(t+1)} = H^{(t)} \cup \left\{ C_a^{(t)} \right\}": "H(t+1) = H(t) U { C_a(t) }",
        r"S_{a, i}^{(t)} = \max\left(-1.0, \min\left(1.0, S_{a, i}^{(t)}\right)\right)": "S_a,i(t) = max(-1.0, min(1.0, S_a,i(t)))",
        r"A_a^{(t)} = \tanh \left( \gamma \cdot A_a^{(t-1)} + \Delta A(E_a^{(t)}) + \begin{bmatrix} 0 \\ 0.2 \cdot Tension_{target} \end{bmatrix} \right)": "A_a(t) = tanh( γ * A_a(t-1) + ΔA(E_a(t)) + [0, 0.2 * Tension_target]^T )",
        r"\Omega = Conviction^{(t-1)} \cdot \left(1 - 0.5 \cdot Flexibility^{(t-1)}\right)": "Ω = Conviction(t-1) * (1 - 0.5 * Flexibility(t-1))",
        r"\lambda_{inertia} = 0.99 - 0.01 \cdot Flexibility^{(t-1)}": "λ_inertia = 0.99 - 0.01 * Flexibility(t-1)",
        r"Stance^{(t)} = \text{clip}\left( Stance^{(t-1)} \cdot \lambda_{inertia} + \Delta Stance(E) \cdot (1 - \Omega) \right)": "Stance(t) = clip( Stance(t-1) * λ_inertia + ΔStance(E) * (1 - Ω) )",
        r"Conviction^{(t)} = \text{clip}_{01}\left( Conviction^{(t-1)} \cdot 0.995 + \Delta Conviction(E) \right)": "Conviction(t) = clip_01( Conviction(t-1) * 0.995 + ΔConviction(E) )",
        r"P_a^{(t)} = \text{clip}\left( P_a^{(t-1)} \cdot 0.99 + \Delta P(E_a^{(t)}) \right)": "P_a(t) = clip( P_a(t-1) * 0.99 + ΔP(E_a(t)) )",
        r"\mathcal{L}_{CE} = -\sum_{i} y_i \log p_i \quad (\text{where } y_i = -100 \text{ is ignored})": "Loss_CE = -sum( y_i * log(p_i) ) (where y_i = -100 is ignored)",
        r"W_{updated} = W_0 + \Delta W = W_0 + BA \quad (\text{where } B \in \mathbb{R}^{d \times r}, A \in \mathbb{R}^{r \times k}, r \ll d, k)": "W_updated = W_0 + ΔW = W_0 + B * A (where B is d x r, A is r x k, r << d, k)",
        r"S_{mel}(m) = \ln \left( \sum_{k=0}^{N-1} |X(k)|^2 \cdot H_m(k) \right)": "S_mel(m) = ln( sum( |X(k)|^2 * H_m(k) ) )",
        r"\text{CER} = \frac{\text{Substitution} + \text{Deletion} + \text{Insertion}}{\text{Reference Length}}": "CER = (Substitution + Deletion + Insertion) / Reference Length",
        r"\text{RMS}_{block} = \sqrt{\frac{1}{N} \sum_{i=1}^{N} x_i^2}": "RMS_block = sqrt( (1 / N) * sum( x_i^2 ) )"
    }

    tex_clean = tex.strip()
    if tex_clean in special_maps:
        return special_maps[tex_clean]

    repl = tex
    repl = repl.replace(r"\mid", "|")
    repl = repl.replace(r"\land", "AND")
    repl = repl.replace(r"\lor", "OR")
    repl = repl.replace(r"\to", "->")
    repl = repl.replace(r"\bullet", "*")
    repl = repl.replace(r"\cup", "U")
    repl = repl.replace(r"\in", "in")
    repl = repl.replace(r"\eta", "η")
    repl = repl.replace(r"\Delta", "Δ")
    repl = repl.replace(r"\lambda", "λ")
    repl = repl.replace(r"\Omega", "Ω")
    repl = repl.replace(r"\rho", "ρ")
    repl = repl.replace(r"\gamma", "γ")
    repl = repl.replace(r"\alpha", "α")
    repl = repl.replace(r"\tau", "τ")
    repl = repl.replace(r"\mathbb{R}", "R")
    repl = repl.replace(r"\mathcal{L}", "Loss")
    repl = repl.replace(r"\mathbf", "")
    repl = repl.replace(r"\text", "")
    repl = repl.replace(r"\tanh", "tanh")
    repl = repl.replace(r"\max", "max")
    repl = repl.replace(r"\min", "min")
    repl = repl.replace(r"\log", "log")
    repl = repl.replace(r"\ln", "ln")
    repl = repl.replace(r"\sqrt", "sqrt")
    repl = repl.replace(r"\left", "")
    repl = repl.replace(r"\right", "")
    repl = repl.replace(r"\quad", " ")
    repl = repl.replace(r"\,", " ")
    repl = repl.replace(r"\{", "{")
    repl = repl.replace(r"\}", "}")
    
    repl = re.sub(r'\^\{(.*?)\}', r'^\1', repl)
    repl = re.sub(r'\_\{(.*?)\}', r'_\1', repl)
    
    return repl

# 모든 README.md 찾기
readme_files = glob.glob('c:/ameva/*/README.md') + glob.glob('c:/ameva/README.md')
for filepath in readme_files:
    if not os.path.exists(filepath):
        continue
        
    print(f"Target file: {filepath}")
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # $$ ... $$ 블록 변환
    def replace_double_dollar(match):
        tex = match.group(1)
        text_math = tex_to_text(tex)
        return f"\n* {text_math}\n"

    # $ ... $ 인라인 변환
    def replace_single_dollar(match):
        tex = match.group(1)
        # 만약 $10%와 같이 수학 기호가 아닌 경우 패스
        if re.match(r'^\d', tex) or tex.endswith('%'):
            return match.group(0)
        return tex_to_text(tex)

    modified = re.sub(r'\$\$(.*?)\$\$', replace_double_dollar, content, flags=re.DOTALL)
    modified = re.sub(r'\$([^\$]+?)\$', replace_single_dollar, modified)
    
    # 1% 미만 복구
    modified = modified.replace("1% 미만 미만", "1% 미만")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(modified)
    print(f"  Successfully processed math variables.")
