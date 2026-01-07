# Kanto Pokédex

<div align="center">

<img width="1658" height="1240" alt="image" src="https://github.com/user-attachments/assets/c0dd0ecf-fe90-4b92-ab4b-f7efe5546072" />



**A modern, responsive Pokédex web application for the original 151 Pokémon**

[English](#english) | [Español](#español)

</div>

---

## English

### 🎯 Overview

Kanto Pokédex Modern is a full-stack web application that showcases all 151 original Pokémon from the Kanto region. Built with modern technologies and a stunning UI/UX design, it offers a premium experience for exploring Pokémon data.

### ✨ Features

- **📱 Responsive Design** - Optimized for mobile, tablet, and desktop
- **🌙 Dark/Light Theme** - Toggle between themes from any page, with system preference detection
- **🔍 Dynamic Search** - Real-time filtering by name, ID, or type
- **🎨 Type-Based Colors** - Cards and backgrounds adapt to Pokémon types
- **📊 Visual Stats** - Animated progress bars with color coding
- **💫 Glassmorphism UI** - Modern frosted glass effect on detail pages
- **⚡ Fast Performance** - Server-side caching prevents API overload
- **🖼️ High-Quality Images** - Official artwork from PokéAPI
- **⚔️ Pokémon Comparator** - Compare 2-6 Pokémon side by side with detailed stats
- **🧬 Evolution Chains** - View complete evolution paths with trigger conditions

### 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | FastAPI (Python 3.11+) |
| **Frontend** | SvelteKit (Svelte 5) |
| **Styling** | Tailwind CSS |
| **HTTP Client** | HTTPX (Async) |
| **Data Source** | [PokéAPI](https://pokeapi.co/) |

### 📁 Project Structure

```
kanto-pokedex/
├── backend/
│   ├── main.py              # FastAPI entry point
│   ├── api/v1/              # API routes
│   ├── models/              # Pydantic models
│   └── services/            # Business logic & caching
│
└── frontend/
    ├── src/
    │   ├── routes/          # SvelteKit pages
    │   └── lib/
    │       ├── components/  # Reusable components
    │       ├── api.ts       # API client
    │       └── theme.svelte.ts  # Theme management
    └── static/
```

### 🎮 Usage

- **Browse** - Scroll through the grid to see all 151 Pokémon
- **Search** - Type in the search bar to filter by name, ID, or type
- **View Details** - Click any card to see full stats and description
- **See Evolutions** - View the complete evolution chain on each Pokémon's detail page
- **Compare Pokémon** - Navigate to `/compare` to compare up to 6 Pokémon side by side
- **Navigate** - Use Previous/Next buttons to browse between Pokémon
- **Toggle Theme** - Click the sun/moon icon to switch themes

---

## Español

### 🎯 Descripción

Kanto Pokédex Modern es una aplicación web full-stack que muestra los 151 Pokémon originales de la región de Kanto. Construida con tecnologías modernas y un diseño UI/UX impresionante, ofrece una experiencia premium para explorar datos Pokémon.

### ✨ Características

- **📱 Diseño Responsivo** - Optimizado para móvil, tablet y escritorio
- **🌙 Tema Oscuro/Claro** - Alterna entre temas desde cualquier página, con detección de preferencia del sistema
- **🔍 Búsqueda Dinámica** - Filtrado en tiempo real por nombre, ID o tipo
- **🎨 Colores por Tipo** - Las tarjetas y fondos se adaptan a los tipos de Pokémon
- **📊 Estadísticas Visuales** - Barras de progreso animadas con código de colores
- **💫 Interfaz Glassmorphism** - Efecto moderno de vidrio esmerilado en páginas de detalle
- **⚡ Alto Rendimiento** - Caché del servidor previene sobrecarga de la API
- **🖼️ Imágenes de Alta Calidad** - Arte oficial de PokéAPI
- **⚔️ Comparador de Pokémon** - Compara de 2 a 6 Pokémon lado a lado con estadísticas detalladas
- **🧬 Cadenas de Evolución** - Visualiza las líneas evolutivas completas con condiciones de evolución

### 🛠️ Stack Tecnológico

| Componente | Tecnología |
|------------|------------|
| **Backend** | FastAPI (Python 3.11+) |
| **Frontend** | SvelteKit (Svelte 5) |
| **Estilos** | Tailwind CSS |
| **Cliente HTTP** | HTTPX (Async) |
| **Fuente de Datos** | [PokéAPI](https://pokeapi.co/) |

### 📁 Estructura del Proyecto

```
kanto-pokedex/
├── backend/
│   ├── main.py              # Punto de entrada FastAPI
│   ├── api/v1/              # Rutas de la API
│   ├── models/              # Modelos Pydantic
│   └── services/            # Lógica de negocio y caché
│
└── frontend/
    ├── src/
    │   ├── routes/          # Páginas SvelteKit
    │   └── lib/
    │       ├── components/  # Componentes reutilizables
    │       ├── api.ts       # Cliente API
    │       └── theme.svelte.ts  # Gestión de temas
    └── static/
```

### 🎮 Uso

- **Explorar** - Desplázate por la cuadrícula para ver los 151 Pokémon
- **Buscar** - Escribe en la barra de búsqueda para filtrar por nombre, ID o tipo
- **Ver Detalles** - Haz clic en cualquier tarjeta para ver estadísticas completas y descripción
- **Ver Evoluciones** - Consulta la cadena evolutiva completa en la página de detalle de cada Pokémon
- **Comparar Pokémon** - Navega a `/compare` para comparar hasta 6 Pokémon lado a lado
- **Navegar** - Usa los botones Anterior/Siguiente para navegar entre Pokémon
- **Cambiar Tema** - Haz clic en el icono de sol/luna para cambiar el tema

---

## � Deployment / Despliegue

### Backend → [Render](https://kanto-pokedex-api-xtpp.onrender.com/docs)
### Frontend → [Vercel](https://kanto-pokedex-jade.vercel.app)
---

## �📄 License / Licencia

MIT License - See [LICENSE](LICENSE) for details.

---

<div align="center">

**Made with ❤️ using [PokéAPI](https://pokeapi.co/)**

</div>
