# Redmine Data Visualizer

Redmine Data Visualizer is a Python application that connects to your Redmine project management system and provides graphical insights into the status and tracker types of issues. This tool helps you monitor your project's progress by visualizing open, closed, bug, feature, and other issue statuses.

---

## Features

- Connect to your Redmine instance using URL and API key.
- Visualize issue statuses with pie charts.
- Display issue tracker distributions with bar charts.
- Store your Redmine credentials securely in a `config.json` file.
- Easy-to-use interface for new or existing users.

---

## Installation

### Prerequisites
- Python 3.8 or higher installed on your system.
- Required Python libraries: 
  - `redminelib`
  - `matplotlib`
  - `tkinter` (usually included in Python's standard library)

### Steps
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/redmine-data-visualizer.git
   cd redmine-data-visualizer
