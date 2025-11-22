import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# ============= STAKEHOLDER MAP (Internal/External, Primary/Secondary) =============
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.set_aspect('equal')

# Draw quadrant lines
ax1.axhline(y=5, color='black', linewidth=2)
ax1.axvline(x=5, color='black', linewidth=2)

# Quadrant labels
ax1.text(2.5, 9, 'INTERNAL\nPRIMARY', ha='center', va='top', fontsize=12, fontweight='bold')
ax1.text(7.5, 9, 'EXTERNAL\nPRIMARY', ha='center', va='top', fontsize=12, fontweight='bold')
ax1.text(2.5, 4.5, 'INTERNAL\nSECONDARY', ha='center', va='top', fontsize=12, fontweight='bold')
ax1.text(7.5, 4.5, 'EXTERNAL\nSECONDARY', ha='center', va='top', fontsize=12, fontweight='bold')

# Internal Primary Stakeholders
stakeholders_int_primary = [
    (1.5, 7.5, 'Healthcare\nEmployees'),
    (3.5, 7.5, 'Nurses\n(4.7M RNs)'),
]

# External Primary Stakeholders
stakeholders_ext_primary = [
    (6.5, 7.5, 'Patients\n(Not Surveyed)'),
]

# Internal Secondary Stakeholders
stakeholders_int_secondary = [
    (1.5, 3, 'Healthcare\nLeadership'),
    (3.5, 3, 'Nursing\nEducators'),
]

# External Secondary Stakeholders
stakeholders_ext_secondary = [
    (6, 3.5, 'Professional\nAssociations'),
    (7, 3.5, 'Staffing\nAgencies'),
    (8, 3.5, 'Academic\nInstitutions'),
    (6.5, 2, 'Technology\nVendors'),
    (8, 2, 'Insurance\nPayers'),
]

# Draw stakeholder boxes
for x, y, label in stakeholders_int_primary:
    box = FancyBboxPatch((x-0.4, y-0.3), 0.8, 0.6, boxstyle="round,pad=0.05", 
                          edgecolor='darkblue', facecolor='lightblue', linewidth=2)
    ax1.add_patch(box)
    ax1.text(x, y, label, ha='center', va='center', fontsize=9, fontweight='bold')

for x, y, label in stakeholders_ext_primary:
    box = FancyBboxPatch((x-0.4, y-0.3), 0.8, 0.6, boxstyle="round,pad=0.05", 
                          edgecolor='darkred', facecolor='lightcoral', linewidth=2)
    ax1.add_patch(box)
    ax1.text(x, y, label, ha='center', va='center', fontsize=9, fontweight='bold')

for x, y, label in stakeholders_int_secondary:
    box = FancyBboxPatch((x-0.4, y-0.3), 0.8, 0.6, boxstyle="round,pad=0.05", 
                          edgecolor='darkblue', facecolor='lightblue', linewidth=1)
    ax1.add_patch(box)
    ax1.text(x, y, label, ha='center', va='center', fontsize=9)

for x, y, label in stakeholders_ext_secondary:
    box = FancyBboxPatch((x-0.4, y-0.3), 0.8, 0.6, boxstyle="round,pad=0.05", 
                          edgecolor='gray', facecolor='lightgray', linewidth=1)
    ax1.add_patch(box)
    ax1.text(x, y, label, ha='center', va='center', fontsize=8)

ax1.set_title('Stakeholder Map\n(Internal/External × Primary/Secondary)', fontsize=14, fontweight='bold', pad=20)
ax1.axis('off')

# ============= POWER/INTEREST DIAGRAM =============
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)
ax2.set_aspect('equal')

# Draw quadrant lines
ax2.axhline(y=5, color='black', linewidth=2)
ax2.axvline(x=5, color='black', linewidth=2)

# Quadrant labels with management strategies
ax2.text(2.5, 9.2, 'KEEP SATISFIED', ha='center', va='top', fontsize=11, fontweight='bold', style='italic', color='purple')
ax2.text(2.5, 8.5, 'High Power, Low Interest', ha='center', va='top', fontsize=9)

ax2.text(7.5, 9.2, 'MANAGE CLOSELY', ha='center', va='top', fontsize=11, fontweight='bold', style='italic', color='darkgreen')
ax2.text(7.5, 8.5, 'High Power, High Interest', ha='center', va='top', fontsize=9)

ax2.text(2.5, 4.7, 'MONITOR', ha='center', va='top', fontsize=11, fontweight='bold', style='italic', color='gray')
ax2.text(2.5, 4, 'Low Power, Low Interest', ha='center', va='top', fontsize=9)

ax2.text(7.5, 4.7, 'KEEP INFORMED', ha='center', va='top', fontsize=11, fontweight='bold', style='italic', color='darkorange')
ax2.text(7.5, 4, 'Low Power, High Interest', ha='center', va='top', fontsize=9)

# Stakeholders with Power/Interest positions
stakeholders_pi = [
    # (x=interest, y=power, label, color)
    # MANAGE CLOSELY: High Power, High Interest
    (7.5, 7.5, 'Healthcare\nLeadership', 'darkgreen'),
    (8.5, 7, 'Senior\nExecutives', 'darkgreen'),
    
    # KEEP SATISFIED: High Power, Low Interest
    (2, 7.5, 'Regulatory\nAgencies', 'purple'),
    (3.5, 7, 'Insurance\nPayers', 'purple'),
    
    # KEEP INFORMED: Low Power, High Interest
    (7, 3, 'Healthcare\nEmployees', 'darkorange'),
    (8.5, 2.5, 'Nurses\n(4.7M)', 'darkorange'),
    (6, 2, 'Patients', 'darkorange'),
    
    # MONITOR: Low Power, Low Interest
    (2.5, 3, 'Technology\nVendors', 'gray'),
    (3.5, 2, 'General\nPublic', 'gray'),
]

# Draw stakeholder circles
for x, y, label, color in stakeholders_pi:
    circle = plt.Circle((x, y), 0.4, color=color, alpha=0.3, linewidth=2, edgecolor=color)
    ax2.add_patch(circle)
    ax2.text(x, y, label, ha='center', va='center', fontsize=9, fontweight='bold')

# Axis labels
ax2.text(5, -0.5, 'INTEREST →', ha='center', fontsize=12, fontweight='bold')
ax2.text(-0.5, 5, 'POWER\n↑', ha='center', va='center', fontsize=12, fontweight='bold', rotation=90)

ax2.set_title('Power/Interest Diagram\n(Stakeholder Management Strategy)', fontsize=14, fontweight='bold', pad=20)
ax2.axis('off')

# Adjust layout and save
plt.tight_layout()
plt.savefig('stakeholder_diagrams.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Stakeholder diagrams saved as 'stakeholder_diagrams.png'")
print("\nStakeholder Map Legend:")
print("- Primary stakeholders: Directly affected by the problem")
print("- Secondary stakeholders: Indirectly affected or influence solution")
print("- Internal: Within healthcare organizations")
print("- External: Outside healthcare organizations")
print("\nPower/Interest Diagram Strategy:")
print("- MANAGE CLOSELY: Key players requiring active engagement")
print("- KEEP SATISFIED: High power but lower interest, keep updated")
print("- KEEP INFORMED: High interest but lower power, engage for feedback")
print("- MONITOR: Minimal effort, periodic communication")
