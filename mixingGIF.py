import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

def capitalTheta(bPerp, g, E, mEffSquare):
    bPerp = bPerp * 1.95e-8
    g = g / 1e6
    return (2 * bPerp * E * g) / mEffSquare

def mEffSquare(axMass, plasmaFreq):
    return axMass**2 - plasmaFreq**2

def calcDeltaEff(L, mEffSquared, E):
    L = L * 1.566e26
    E = E * 1e3
    return (mEffSquared * L) / (4 * E)

def probability(axMass, bPerp, g, L, E):
    mEffSquared = mEffSquare(axMass, plasmaFreq)
    capTheta = capitalTheta(bPerp, g, E, mEffSquared)
    capThetaSquare = capTheta**2
    deltaEff = calcDeltaEff(L, mEffSquared, E)
    first = capThetaSquare / (1 + capThetaSquare)
    second = np.sin(deltaEff * np.sqrt(1 + capThetaSquare))**2
    return first * second

#Constants

plasmaFreq = 1e-12

# Initial (log10 values)
log_m_start = -11.7
log_m_end   = -11.3

log_g_start = -11.5
log_g_end   = -11.0

log_B_start = 0.5
log_B_end   = 1.0

log_L = 2.5  # fixed

# Energy range
E = np.linspace(1, 12, 500)
L = 10**log_L

#Plotting

fig, ax = plt.subplots(figsize=(8, 5))
line, = ax.plot([], [], lw=2)

ax.set_xlim(1, 12)
ax.set_ylim(0, 1)
ax.set_xlabel("Energy [keV]", fontsize=12)
ax.set_ylabel("P", fontsize=12)
ax.set_title("ALP Mixing Probability", fontsize=14)

#Labels
text_g = ax.text(0.02, 0.95, "", transform=ax.transAxes,
                 color="red", fontsize=14, weight='bold')
text_m = ax.text(0.02, 0.90, "", transform=ax.transAxes,
                 color="blue", fontsize=14, weight='bold')
text_B = ax.text(0.02, 0.85, "", transform=ax.transAxes,
                 color="green", fontsize=14, weight='bold')
text_L = ax.text(0.02, 0.80, "", transform=ax.transAxes,
                 color="black", fontsize=13)

#frames

N = 50

frames_g = np.linspace(log_g_start, log_g_end, N)
frames_m = np.linspace(log_m_start, log_m_end, N)
frames_B = np.linspace(log_B_start, log_B_end, N)

total_frames = 3 * N

#Animation

def animate(i):

    #g
    if i < N:
        log_g = frames_g[i]
        log_m = log_m_start
        log_B = log_B_start
        color = "red"

    #m
    elif i < 2*N:
        log_g = log_g_end
        log_m = frames_m[i - N]
        log_B = log_B_start
        color = "blue"

    #B
    else:
        log_g = log_g_end
        log_m = log_m_end
        log_B = frames_B[i - 2*N]
        color = "green"

    #Convert to linear
    m = 10**log_m
    g = 10**log_g
    B = 10**log_B

    #Compute probability
    P = probability(m, B, g, L, E)

    #Update plot
    line.set_data(E, P)
    line.set_color(color)

    #Update text
    text_g.set_text(rf"$\log_{{10}}(g_{{a\gamma}}) = {log_g:.3f}$")
    text_m.set_text(rf"$\log_{{10}}(m_a) = {log_m:.3f}$")
    text_B.set_text(rf"$\log_{{10}}(B_\perp) = {log_B:.3f}$")
    text_L.set_text(rf"$\log_{{10}}(L) = {log_L:.1f}$")

    return line, text_g, text_m, text_B, text_L

#Body

anim = FuncAnimation(fig, animate, frames=total_frames, interval=80)

anim.save("alp_animation_transitions.gif", writer=PillowWriter(fps=15))

plt.show()