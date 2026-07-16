# CalPro Project Design Pattern

Follow this design aesthetic for all frontend development in the CalPro project:

1. **Overall Theme**: Premium, modern, glassmorphic UI.
2. **Color Palette**: 
   - Primary: `#6366f1` (Indigo/Purple blend)
   - Accent/Warning: `#f59e0b` (Amber/Orange)
   - Backgrounds: Use `#f1f5f9` with subtle multi-color radial-gradients.
3. **Glassmorphism**: Use translucent backgrounds `rgba(255, 255, 255, 0.6 to 0.85)` with `backdrop-filter: blur(...)` for navbars, cards, and forms.
4. **Typography**: Use the 'Outfit' font (weights 300 to 800) for a clean, geometric, modern look. Use `.fw-bold` and `.fw-semibold` liberally for emphasis.
5. **UI Components**:
   - Buttons should have gradients (e.g., `linear-gradient(135deg, var(--brand-primary), #4338ca)`) with hover lift effects (`transform: translateY(-2px)`).
   - Inputs should be slightly transparent, gaining a solid white background and primary border on focus.
   - Text gradients: Use `-webkit-background-clip: text` for impactful headings.
6. **Layouts**: Prefer two-column split layouts for heroes. Use subtle CSS animations (like `.float` or `.wave`) to make the interface feel dynamic and alive.
