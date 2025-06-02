# Media Workflow Toolbox 🎥 📸

A collection of powerful CLI tools and utilities for photographers and videographers to streamline their media workflow.

[English](#english) | [Español](#español)

---

## English

### 🎯 Overview

Media Workflow Toolbox is a suite of command-line tools designed to automate common tasks in photo and video workflows. Built with Python, it offers a modern terminal user interface and efficient file operations.

### ✨ Features

- **File Sorter**: Automatically organize media files into categorized folders
- **Folder Compare**: Find missing or unmatched files between directories
- **Project Generator**: Create standardized folder structures for photo/video projects
- Rich terminal UI with progress indicators
- Detailed logging of all operations
- Cross-platform compatibility (Windows, Linux)

### 🚀 Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/media-workflow-toolbox.git
cd media-workflow-toolbox
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

### 💻 Usage

1. Start the toolbox interface:
```bash
python toolbox.py
```

2. Or run individual scripts directly:
```bash
python scripts/file_sorter.py --help
python scripts/folder_compare.py --help
python scripts/project_generator.py --help
```

### 📖 Tool Documentation

#### File Sorter
Organizes files into categorized folders based on their extensions.
```bash
python scripts/file_sorter.py <source_directory>
```

#### Folder Compare
Compare two directories and show missing or unmatched files.
```bash
python scripts/folder_compare.py <source_dir> <target_dir> [--check-content]
```

#### Project Generator
Create standardized folder structures for new projects.
```bash
python scripts/project_generator.py <project_name> [--template photo_basic|video_basic]
```

### 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

---

## Español

### 🎯 Descripción General

Media Workflow Toolbox es un conjunto de herramientas de línea de comandos diseñadas para automatizar tareas comunes en flujos de trabajo de fotografía y video. Construido con Python, ofrece una interfaz moderna de terminal y operaciones eficientes de archivos.

### ✨ Características

- **Organizador de Archivos**: Organiza automáticamente archivos multimedia en carpetas categorizadas
- **Comparador de Carpetas**: Encuentra archivos faltantes o no coincidentes entre directorios
- **Generador de Proyectos**: Crea estructuras de carpetas estandarizadas para proyectos
- Interfaz de terminal rica con indicadores de progreso
- Registro detallado de todas las operaciones
- Compatibilidad multiplataforma (Windows, Linux)

### 🚀 Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/yourusername/media-workflow-toolbox.git
cd media-workflow-toolbox
```

2. Crea un entorno virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

### 💻 Uso

1. Inicia la interfaz de herramientas:
```bash
python toolbox.py
```

2. O ejecuta scripts individuales directamente:
```bash
python scripts/file_sorter.py --help
python scripts/folder_compare.py --help
python scripts/project_generator.py --help
```

### 📖 Documentación de Herramientas

#### Organizador de Archivos
Organiza archivos en carpetas categorizadas según sus extensiones.
```bash
python scripts/file_sorter.py <directorio_origen>
```

#### Comparador de Carpetas
Compara dos directorios y muestra archivos faltantes o no coincidentes.
```bash
python scripts/folder_compare.py <dir_origen> <dir_destino> [--check-content]
```

#### Generador de Proyectos
Crea estructuras de carpetas estandarizadas para nuevos proyectos.
```bash
python scripts/project_generator.py <nombre_proyecto> [--template photo_basic|video_basic]
```

### 🤝 Contribuir

1. Haz un fork del repositorio
2. Crea una rama para tu función
3. Realiza tus cambios
4. Sube los cambios a la rama
5. Crea un Pull Request

---

## 📝 License / Licencia

MIT License / Licencia MIT

## 🙏 Acknowledgments / Agradecimientos

- Rich library for beautiful terminal formatting
- Typer for CLI interfaces
- Textual for TUI components 