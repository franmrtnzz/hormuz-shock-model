# Hormuz Strait Supply Shock Model

A small macroeconomic simulation of a negative supply shock caused by a hypothetical closure of the Strait of Hormuz.

The script uses a three-equation New Keynesian framework to show how a supply shock can move inflation, output, and the policy rate under a Taylor-rule response.

## Model

| Block | Equation | Role |
| --- | --- | --- |
| Phillips curve | `pi_t = pi_(t-1) + gamma * y_t + epsilon_t` | Inflation dynamics |
| IS curve | `y_t = -alpha * (r_t - r*)` | Output gap response |
| Taylor rule | `r_t = r* + phi_pi * (pi_t - pi*) + phi_y * y_t` | Policy-rate reaction |

## Output

The script generates a two-panel chart:

- Monetary policy rule: interest-rate response to the shock.
- Aggregate supply/demand: inflation and output-gap dynamics.

![Hormuz supply shock output](hormuz_oa_da_taylor.png)

## Parameters

| Parameter | Value | Description |
| --- | --- | --- |
| `pi*` | 2.0% | Inflation target |
| `r*` | 1.0% | Natural real interest rate |
| `phi_pi` | 1.5 | Taylor-rule coefficient on inflation |
| `phi_y` | 0.5 | Taylor-rule coefficient on the output gap |
| `gamma` | 0.4 | Phillips-curve slope |
| `epsilon` | 3.0 pp | Supply-shock magnitude |

## Usage

```bash
pip install numpy matplotlib
python hormuz_oa_da_model.py
```

## License

MIT
