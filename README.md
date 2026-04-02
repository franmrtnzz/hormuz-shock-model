# Hormuz Strait Supply Shock — OA/DA Model with Taylor Rule

Simulation of a **negative supply shock** (closure of the Strait of Hormuz) using a 3-equation New Keynesian framework:

| Equation | Description |
|---|---|
| OA (Phillips Curve) | $\pi_t = \pi_{t-1} + \gamma \cdot y_t + \varepsilon_t$ |
| IS (Aggregate Demand) | $y_t = -\alpha \cdot (r_t - r^*)$ |
| RPM (Taylor Rule) | $r_t = r^* + \varphi_\pi (\pi_t - \pi^*) + \varphi_y \cdot y_t$ |

## Output

The script generates a combined chart showing:
- **Left panel**: Monetary Policy Rule (RPM) — interest rate response
- **Right panel**: OA/DA — inflation and output gap dynamics

![Hormuz OA/DA Taylor](hormuz_oa_da_taylor.png)

## Parameters

| Parameter | Value | Description |
|---|---|---|
| π* | 2.0% | Inflation target |
| r* | 1.0% | Natural real interest rate |
| φ_π | 1.5 | Taylor coefficient on inflation |
| φ_y | 0.5 | Taylor coefficient on output gap |
| γ | 0.4 | Phillips curve slope |
| ε | 3.0 pp | Supply shock magnitude |

## Usage

```bash
pip install numpy matplotlib
python hormuz_oa_da_model.py
```

## License

MIT
