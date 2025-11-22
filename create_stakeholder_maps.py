import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# ===== STAKEHOLDER MAP (Concentric Circles) =====
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 10)
ax1.set_aspect('equal')

# Draw concentric circles
circle_external = plt.Circle((5, 5), 4, color='lightgray', alpha=0.3, label='External')
circle_connected = plt.Circle((5, 5), 2.8, color='darkgray', alpha=0.4, label='Connected')
circle_internal = plt.Circle((5, 5), 1.8, color='gray', alpha=0.5, label='Internal')

ax1.add_patch(circle_external)
ax1.add_patch(circle_connected)
ax1.add_patch(circle_internal)

# Add labels in circles
ax1.text(5, 5, 'Internal', ha='center', va='center', fontsize=12, weight='bold')
ax1.text(5, 7.3, 'Connected', ha='center', va='center', fontsize=12, weight='bold')
ax1.text(5, 8.8, 'External', ha='center', va='center', fontsize=12, weight='bold')

# Add axes labels
ax1.text(0.5, 5, 'Impact of the\ndecision on them\n\nDirect', 
         ha='center', va='center', fontsize=10, rotation=90)
ax1.text(0.5, 2, 'Indirect', ha='center', va='center', fontsize=10, style='italic', rotation=90)

ax1.text(5, 0.5, 'Primary', ha='center', va='bottom', fontsize=10)
ax1.text(9, 0.5, 'Secondary', ha='right', va='bottom', fontsize=10)
ax1.text(8, 0.8, 'Responsibility of\nthe organisation\ntowards them', 
         ha='center', va='bottom', fontsize=9)

# Draw axes lines
ax1.axhline(y=5, color='gray', linestyle='--', linewidth=1, alpha=0.5)
ax1.axvline(x=5, color='gray', linestyle='--', linewidth=1, alpha=0.5)

# Add stakeholders to map
# Internal stakeholders
ax1.text(5, 5.5, '• Healthcare\n  Employees', ha='center', va='center', fontsize=8, color='darkblue')
ax1.text(5, 4.5, '• Leadership/\n  Management', ha='center', va='center', fontsize=8, color='darkblue')

# Connected stakeholders
ax1.text(3.5, 7, '• Patients', ha='center', va='center', fontsize=8, color='darkgreen')
ax1.text(6.5, 6.8, '• Staffing\n  Agencies', ha='center', va='center', fontsize=8, color='darkgreen')
ax1.text(3.5, 6, '• Academic\n  Institutions', ha='center', va='center', fontsize=8, color='darkgreen')

# External stakeholders
ax1.text(2.5, 8.5, '• Professional\n  Associations', ha='center', va='center', fontsize=8, color='darkred')
ax1.text(7.5, 8.3, '• Regulatory\n  Agencies', ha='center', va='center', fontsize=8, color='darkred')
ax1.text(5, 8.9, '• Insurance\n  Payers', ha='center', va='center', fontsize=8, color='darkred')
ax1.text(3, 2.5, '• Technology\n  Vendors', ha='center', va='center', fontsize=8, color='darkred')
ax1.text(7, 2.8, '• Local\n  Community', ha='center', va='center', fontsize=8, color='darkred')

ax1.set_title('Stakeholder Map: Healthcare Workforce Burnout/Turnover Crisis', 
              fontsize=14, weight='bold', pad=20)
ax1.axis('off')

# ===== POWER/INTEREST DIAGRAM =====
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 10)

# Draw quadrants with colors
ax2.add_patch(plt.Rectangle((0, 5), 5, 5, facecolor='#ffe6e6', alpha=0.3))  # Keep Satisfied
ax2.add_patch(plt.Rectangle((5, 5), 5, 5, facecolor='#ffcccc', alpha=0.5))  # Manage Closely
ax2.add_patch(plt.Rectangle((0, 0), 5, 5, facecolor='#f0f0f0', alpha=0.3))  # Monitor
ax2.add_patch(plt.Rectangle((5, 0), 5, 5, facecolor='#ffe6cc', alpha=0.3))  # Keep Informed

# Add quadrant labels
ax2.text(2.5, 9.3, 'Keep Satisfied\n(High Power, Low Interest)', 
         ha='center', va='top', fontsize=10, weight='bold', color='darkred')
ax2.text(7.5, 9.3, 'Manage Closely\n(High Power, High Interest)', 
         ha='center', va='top', fontsize=10, weight='bold', color='darkred')
ax2.text(2.5, 0.7, 'Monitor\n(Low Power, Low Interest)', 
         ha='center', va='bottom', fontsize=10, weight='bold', color='gray')
ax2.text(7.5, 0.7, 'Keep Informed\n(Low Power, High Interest)', 
         ha='center', va='bottom', fontsize=10, weight='bold', color='darkorange')

# Define stakeholders with their positions
stakeholders = [
    # High Power, High Interest (Manage Closely)
    ('Healthcare\nLeadership', 8.5, 8.5, 'red'),
    ('Senior\nExecutives', 7.5, 8, 'red'),
    ('Hospital\nAdministrators', 8, 7, 'red'),
    
    # High Power, Low Interest (Keep Satisfied)
    ('Regulatory\nAgencies', 2.5, 8, 'orange'),
    ('Insurance\nPayers', 3.5, 7.5, 'orange'),
    
    # Low Power, High Interest (Keep Informed)
    ('Healthcare\nEmployees', 8, 3.5, 'green'),
    ('Nurses', 7.5, 3, 'green'),
    ('Physicians', 8.5, 2.5, 'green'),
    ('Patients', 7, 4, 'green'),
    
    # Low Power, Low Interest (Monitor)
    ('Technology\nVendors', 2, 2.5, 'gray'),
    ('Staffing\nAgencies', 3, 3.5, 'gray'),
    ('Local\nCommunity', 1.5, 1.5, 'gray'),
    ('Academic\nInstitutions', 3.5, 2, 'gray'),
    
    # Medium positions
    ('Professional\nAssociations', 4, 6, 'purple'),
    ('Mid-Level\nManagers', 6, 6.5, 'darkred'),
]

# Plot stakeholders
for name, x, y, color in stakeholders:
    ax2.scatter(x, y, s=200, c=color, alpha=0.6, edgecolors='black', linewidth=1.5)
    ax2.text(x, y, name, ha='center', va='center', fontsize=7, weight='bold', color='white')

# Add axes labels
ax2.set_xlabel('INTEREST →', fontsize=12, weight='bold')
ax2.set_ylabel('POWER →', fontsize=12, weight='bold')
ax2.text(5, -0.8, 'Low Interest                                                 High Interest', 
         ha='center', va='top', fontsize=9, style='italic')
ax2.text(-0.8, 5, 'Low\nPower', ha='right', va='center', fontsize=9, style='italic', rotation=90)
ax2.text(-0.8, 8, 'High\nPower', ha='right', va='top', fontsize=9, style='italic', rotation=90)

# Draw grid lines
ax2.axhline(y=5, color='black', linestyle='-', linewidth=2)
ax2.axvline(x=5, color='black', linestyle='-', linewidth=2)
ax2.grid(True, alpha=0.2)

ax2.set_title('Power/Interest Diagram: Healthcare Workforce Crisis Stakeholders', 
              fontsize=14, weight='bold', pad=20)
ax2.set_xticks([])
ax2.set_yticks([])

plt.tight_layout()
plt.savefig('stakeholder_diagrams.png', dpi=300, bbox_inches='tight', facecolor='white')
print("Stakeholder diagrams created successfully: stakeholder_diagrams.png")
plt.close()

# Create a text description file
with open('stakeholder_mapping_description.txt', 'w') as f:
    f.write("STAKEHOLDER MAPPING FOR HEALTHCARE WORKFORCE BURNOUT/TURNOVER CRISIS\n")
    f.write("="*80 + "\n\n")
    
    f.write("STAKEHOLDER MAP (Concentric Circles)\n")
    f.write("-"*40 + "\n\n")
    f.write("INTERNAL STAKEHOLDERS (Direct Impact, Primary Responsibility):\n")
    f.write("• Healthcare Employees (nurses, physicians, clinical staff)\n")
    f.write("  - Directly experiencing burnout and making turnover decisions\n")
    f.write("  - Primary responsibility: Organization's core workforce\n\n")
    f.write("• Leadership/Management\n")
    f.write("  - Directly impacted by retention costs and implementation responsibility\n")
    f.write("  - Primary responsibility: Decision-makers and intervention implementers\n\n")
    
    f.write("CONNECTED STAKEHOLDERS (Direct/Indirect Impact, Primary/Secondary Responsibility):\n")
    f.write("• Patients\n")
    f.write("  - Directly impacted by care quality and continuity\n")
    f.write("  - Primary responsibility: Service recipients\n\n")
    f.write("• Staffing Agencies\n")
    f.write("  - Direct impact through temporary placement demand\n")
    f.write("  - Secondary responsibility: Workforce suppliers\n\n")
    f.write("• Academic Institutions\n")
    f.write("  - Indirect impact through training disruption\n")
    f.write("  - Secondary responsibility: Education partners\n\n")
    
    f.write("EXTERNAL STAKEHOLDERS (Indirect Impact, Secondary Responsibility):\n")
    f.write("• Professional Associations (AACN, ANA, AMA)\n")
    f.write("  - Indirect impact, advocacy role\n")
    f.write("  - Secondary responsibility: Professional representation\n\n")
    f.write("• Regulatory Agencies (JCAHO, CMS)\n")
    f.write("  - Indirect impact through quality standards\n")
    f.write("  - Secondary responsibility: Oversight bodies\n\n")
    f.write("• Insurance Payers\n")
    f.write("  - Indirect impact through quality and cost\n")
    f.write("  - Secondary responsibility: Reimbursement entities\n\n")
    f.write("• Technology Vendors\n")
    f.write("  - Indirect impact (EHR administrative burden)\n")
    f.write("  - Secondary responsibility: System suppliers\n\n")
    f.write("• Local Community\n")
    f.write("  - Indirect impact through healthcare access\n")
    f.write("  - Secondary responsibility: Society at large\n\n")
    
    f.write("\n" + "="*80 + "\n\n")
    f.write("POWER/INTEREST DIAGRAM QUADRANTS\n")
    f.write("-"*40 + "\n\n")
    
    f.write("MANAGE CLOSELY (High Power, High Interest):\n")
    f.write("• Healthcare Leadership/Senior Executives/Hospital Administrators\n")
    f.write("  - Control resources and budgets for interventions\n")
    f.write("  - Directly impacted by turnover costs ($52,350 per RN)\n")
    f.write("  - Accountable for workforce crisis resolution\n")
    f.write("  - Strategy: Engage deeply in decision-making, regular updates\n\n")
    
    f.write("KEEP SATISFIED (High Power, Low Interest):\n")
    f.write("• Regulatory Agencies (JCAHO, CMS)\n")
    f.write("  - High power through accreditation and reimbursement\n")
    f.write("  - Lower interest (not focused on this specific issue)\n")
    f.write("• Insurance Payers\n")
    f.write("  - Financial leverage but may prioritize other quality metrics\n")
    f.write("  - Strategy: Keep satisfied, meet their requirements\n\n")
    
    f.write("KEEP INFORMED (Low Power, High Interest):\n")
    f.write("• Healthcare Employees (Nurses, Physicians, Clinical Staff)\n")
    f.write("  - Directly experiencing burnout (32% above baseline)\n")
    f.write("  - Limited organizational decision authority\n")
    f.write("  - High interest in solutions that reduce workload\n")
    f.write("• Patients\n")
    f.write("  - Affected by care quality but limited organizational influence\n")
    f.write("  - Strategy: Transparent communication, gather feedback\n\n")
    
    f.write("MONITOR (Low Power, Low Interest):\n")
    f.write("• Technology Vendors\n")
    f.write("  - Peripheral involvement unless workflow changes required\n")
    f.write("• Staffing Agencies\n")
    f.write("  - Benefit from status quo (turnover creates demand)\n")
    f.write("• Local Community\n")
    f.write("  - Broad concern but not focused on specific issue\n")
    f.write("• Academic Institutions\n")
    f.write("  - Affected by clinical placement disruption but limited power\n")
    f.write("  - Strategy: Monitor, minimal effort\n\n")
    
    f.write("MEDIUM POSITIONS:\n")
    f.write("• Professional Associations (AACN, ANA, AMA)\n")
    f.write("  - Moderate power through advocacy\n")
    f.write("  - High interest in workforce well-being\n")
    f.write("• Mid-Level Managers\n")
    f.write("  - Moderate power (implement but don't set strategy)\n")
    f.write("  - High interest (responsible for daily operations)\n")

print("Stakeholder mapping description created: stakeholder_mapping_description.txt")
