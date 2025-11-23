"""
Chart widgets using Matplotlib for data visualization
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QSizePolicy
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class TypePieChart(QGroupBox):
    """Pie chart widget for equipment type distribution"""
    
    def __init__(self):
        super().__init__("Type Distribution")
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        
        # Create matplotlib figure and canvas
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ax = self.figure.add_subplot(111)
        
        # Initial empty state
        self.show_no_data()
        
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
    def show_no_data(self):
        """Display 'No data available' message"""
        self.ax.clear()
        self.ax.text(0.5, 0.5, 'No data available\n\nUpload a CSV file to see visualization', 
                    ha='center', va='center', 
                    transform=self.ax.transAxes,
                    fontsize=12, color='#6c757d',
                    bbox=dict(boxstyle='round,pad=1', facecolor='#f8f9fa', edgecolor='#e9ecef', linewidth=2))
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        self.ax.set_facecolor('#ffffff')
        self.figure.patch.set_facecolor('#ffffff')
        self.figure.tight_layout()
        self.canvas.draw()
        
    def update_chart(self, type_distribution):
        """
        Update pie chart with new data
        
        Args:
            type_distribution: Dict mapping equipment types to counts
        """
        self.ax.clear()
        
        if not type_distribution or len(type_distribution) == 0:
            self.show_no_data()
            return
        
        # Prepare data
        labels = list(type_distribution.keys())
        sizes = list(type_distribution.values())
        
        # Create modern color palette with gradients
        colors = ['#667eea', '#f093fb', '#4facfe', '#fa709a', '#30cfd0', 
                  '#f5576c', '#4facfe', '#43e97b', '#fa709a', '#fee140']
        chart_colors = colors[:len(labels)]
        
        # Create pie chart with modern styling
        wedges, texts, autotexts = self.ax.pie(
            sizes, 
            labels=labels, 
            autopct='%1.1f%%',
            colors=chart_colors, 
            startangle=90,
            textprops={'fontsize': 10, 'weight': 'bold'},
            wedgeprops={'edgecolor': 'white', 'linewidth': 2}
        )
        
        # Make percentage text bold and white
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
        
        # Style labels
        for text in texts:
            text.set_fontsize(11)
            text.set_weight('600')
        
        self.ax.axis('equal')
        self.figure.patch.set_facecolor('#ffffff')
        self.figure.tight_layout()
        self.canvas.draw()


class FlowrateChart(QGroupBox):
    """Line chart widget for flowrate data visualization"""
    
    def __init__(self):
        super().__init__("Flowrate Data (Sample)")
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface"""
        layout = QVBoxLayout()
        
        # Create matplotlib figure and canvas
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ax = self.figure.add_subplot(111)
        
        # Initial empty state
        self.show_no_data()
        
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
    def show_no_data(self):
        """Display 'No data available' message"""
        self.ax.clear()
        self.ax.text(0.5, 0.5, 'No data available\n\nUpload a CSV file to see visualization', 
                    ha='center', va='center', 
                    transform=self.ax.transAxes,
                    fontsize=12, color='#6c757d',
                    bbox=dict(boxstyle='round,pad=1', facecolor='#f8f9fa', edgecolor='#e9ecef', linewidth=2))
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_visible(False)
        self.ax.spines['left'].set_visible(False)
        self.ax.set_facecolor('#ffffff')
        self.figure.patch.set_facecolor('#ffffff')
        self.figure.tight_layout()
        self.canvas.draw()
        
    def update_chart(self, rows):
        """
        Update line chart with new data
        
        Args:
            rows: List of equipment data dictionaries
        """
        self.ax.clear()
        
        if not rows or len(rows) == 0:
            self.show_no_data()
            return
        
        # Extract equipment names and flowrates
        equipment_names = []
        flowrates = []
        
        for i, row in enumerate(rows):
            # Handle different possible column names
            name = row.get('Equipment Name') or row.get('Equipment') or f"Item {i+1}"
            equipment_names.append(name)
            
            # Get flowrate value
            flowrate = row.get('Flowrate', 0)
            try:
                flowrates.append(float(flowrate))
            except (ValueError, TypeError):
                flowrates.append(0)
        
        # Create line chart
        x_pos = range(len(flowrates))
        self.ax.plot(x_pos, flowrates, 
                    marker='o', 
                    linewidth=2.5, 
                    markersize=8,
                    color='#3498db', 
                    markerfacecolor='#2980b9',
                    markeredgewidth=2,
                    markeredgecolor='white',
                    label='Flowrate')
        
        # Styling
        self.ax.set_xlabel('Equipment', fontsize=11, fontweight='bold')
        self.ax.set_ylabel('Flowrate', fontsize=11, fontweight='bold')
        self.ax.set_title('Flowrate by Equipment', fontsize=12, fontweight='bold', pad=15)
        self.ax.grid(True, alpha=0.3, linestyle='--')
        self.ax.legend(loc='upper right', framealpha=0.9)
        
        # Set x-axis labels
        if len(equipment_names) <= 15:
            self.ax.set_xticks(x_pos)
            self.ax.set_xticklabels(equipment_names, rotation=45, ha='right', fontsize=9)
        else:
            # Too many labels - show every nth label
            step = len(equipment_names) // 10 + 1
            self.ax.set_xticks(x_pos[::step])
            self.ax.set_xticklabels([equipment_names[i] for i in range(0, len(equipment_names), step)],
                                   rotation=45, ha='right', fontsize=9)
        
        # Add value labels on points for small datasets
        if len(flowrates) <= 10:
            for i, (x, y) in enumerate(zip(x_pos, flowrates)):
                self.ax.annotate(f'{y:.1f}', 
                               xy=(x, y), 
                               xytext=(0, 10),
                               textcoords='offset points',
                               ha='center',
                               fontsize=9,
                               fontweight='600',
                               color='#495057',
                               bbox=dict(boxstyle='round,pad=0.4', 
                                       facecolor='#fef5e7', 
                                       edgecolor='#f5c26b',
                                       alpha=0.9,
                                       linewidth=1.5))
        
        self.figure.tight_layout()
        self.canvas.draw()