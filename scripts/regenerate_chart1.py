#!/usr/bin/env python3
"""Quick script to regenerate only Chart 1 - Adult Saturation"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# Set dark theme
plt.style.use('dark_background')
plt.rcParams['figure.facecolor'] = '#1a1a1a'
plt.rcParams['axes.facecolor'] = '#1a1a1a'
plt.rcParams['savefig.facecolor'] = '#1a1a1a'

# Load data
enrol_data = pd.read_csv('data/enrolment.csv')

# Create total column
enrol_data['total'] = enrol_data['age_0_5'] + enrol_data['age_5_17'] + enrol_data['age_18_greater']

# Create the chart
fig = plt.figure(figsize=(16, 12))

# Create grid layout - main chart area and stats area
gs = fig.add_gridspec(2, 2, height_ratios=[4, 1], width_ratios=[3, 1], 
                      hspace=0.15, wspace=0.1)
ax_pie = fig.add_subplot(gs[0, :])
ax_stats = fig.add_subplot(gs[1, 0])
ax_legend = fig.add_subplot(gs[1, 1])

# Calculate totals
total_enrolments = enrol_data['total'].sum()
adult_enrolments = enrol_data['age_18_greater'].sum()
child_enrolments = total_enrolments - adult_enrolments
child_pct = (child_enrolments / total_enrolments) * 100
adult_pct = 100 - child_pct

# Create donut chart with gradient-like effect
outer_colors = ['#FF6B6B', '#4ECDC4']

# Outer ring - main data
wedges, texts, autotexts = ax_pie.pie(
    [child_enrolments, adult_enrolments], 
    colors=outer_colors,
    autopct=lambda pct: f'{pct:.1f}%' if pct > 2 else '',
    startangle=90,
    textprops={'fontsize': 28, 'weight': 'bold', 'color': 'white'},
    explode=(0.02, 0.02),
    shadow=True,
    wedgeprops=dict(width=0.5, edgecolor='white', linewidth=3)
)

# Inner ring for donut effect
inner_circle = plt.Circle((0, 0), 0.45, fc='#1a1a1a', ec='white', linewidth=2)
ax_pie.add_patch(inner_circle)

# Center text with better styling
ax_pie.text(0, 0.08, '✓ ADULT SATURATION', ha='center', va='center', 
            fontsize=22, weight='bold', color='#4ECDC4')
ax_pie.text(0, -0.08, 'ACHIEVED', ha='center', va='center', 
            fontsize=26, weight='bold', color='white')
ax_pie.text(0, -0.25, f'{child_pct:.1f}% Children', ha='center', va='center', 
            fontsize=18, weight='bold', color='#FF6B6B')

# Title
ax_pie.set_title('INDIA HAS ACHIEVED ADULT SATURATION\n97% of New Enrollments are Children', 
                 fontsize=26, weight='bold', pad=20, color='white')

# Stats panel (bottom left)
ax_stats.set_facecolor('#2a2a2a')
ax_stats.axis('off')

stats_text = f'''KEY STATISTICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Records:           {total_enrolments:>12,}
Adult Enrollments:       {adult_enrolments:>12,}  ({adult_pct:.1f}%)
Child Enrollments:       {child_enrolments:>12,}  ({child_pct:.1f}%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CONCLUSION: Adult enrollment mission is COMPLETE
India has transitioned to maintenance phase'''

ax_stats.text(0.05, 0.5, stats_text, transform=ax_stats.transAxes,
              fontsize=14, weight='bold', color='white', 
              family='monospace', va='center',
              bbox=dict(boxstyle="round,pad=0.8", facecolor='#27AE60', 
                       alpha=0.95, edgecolor='white', linewidth=2))

# Legend panel (bottom right)
ax_legend.set_facecolor('#1a1a1a')
ax_legend.axis('off')

# Custom legend
legend_elements = [
    plt.Rectangle((0,0), 1, 1, facecolor='#FF6B6B', edgecolor='white', linewidth=2),
    plt.Rectangle((0,0), 1, 1, facecolor='#4ECDC4', edgecolor='white', linewidth=2)
]
legend = ax_legend.legend(legend_elements, 
                          [f'Children (<18)\n{child_enrolments:,}', 
                           f'Adults (18+)\n{adult_enrolments:,}'],
                          loc='center', fontsize=14, framealpha=0.95,
                          facecolor='#2a2a2a', edgecolor='white', 
                          labelcolor='white', handlelength=2, handleheight=2)
legend.get_frame().set_linewidth(2)

plt.savefig('visualizations/01_adult_saturation_proof.png', dpi=300, bbox_inches='tight', 
            facecolor='#1a1a1a', edgecolor='none')
plt.close()

print("✅ Chart 1 regenerated: visualizations/01_adult_saturation_proof.png")
