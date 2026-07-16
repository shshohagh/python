# Add Remaining Features (Phase 3)

The remaining features to be added to the project are:
1. **Food Database API Integration**
2. **Charts & Analytics**

## Open Questions

- **Food Database**: I plan to use the open and free **OpenFoodFacts API**. It doesn't require any API key and provides basic nutrition facts. Do you have any preference for another API (like Nutritionix or Edamam, which require API keys)?
- **Charts Location**: Do you want the charts displayed on a separate "Analytics" page, or directly integrated at the bottom of the "Dashboard"? My proposal below creates a dedicated Analytics page to keep the dashboard clean.

## Proposed Changes

### CalApp Component

#### [MODIFY] views.py
- Add `analytics_view(request)` which will calculate and return calorie and macronutrient data for the last 7 days.
- Format this data appropriately so Chart.js can consume it directly on the frontend.

#### [MODIFY] urls.py
- Add `path('analytics/', views.analytics_view, name='analytics')`.

#### [MODIFY] templates/CalApp/base.html
- Include `Chart.js` via CDN.
- Add an "Analytics" link to the navigation bar.

#### [NEW] templates/CalApp/analytics.html
- Create a new template with beautiful glassmorphic cards (following `AGENTS.md`).
- Implement `Chart.js` line charts to visualize Calorie Intake vs BMR over the last 7 days.
- Implement a bar/doughnut chart for Macronutrient distribution.

#### [MODIFY] templates/CalApp/dashboard.html
- Update the "Log Food" modal to include a "Search Food" input field and a "Search" button.
- Add custom JavaScript to query the OpenFoodFacts API when the user searches for a food item.
- Upon selecting an item from the search results, automatically fill in the `item_name`, `calories`, `protein`, `carbs`, and `fats` input fields in the form.

## Verification Plan
### Manual Verification
- Go to the Dashboard, open the "Log Food" modal, type a food name like "Apple" and hit search. Click a result and verify it populates the form fields correctly.
- Go to the new "Analytics" page and verify the charts render properly with accurate data for the current user.
