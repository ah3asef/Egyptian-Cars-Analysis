# Egyptian Cars Analysis - Complete Project Documentation

## Project Overview
This project performs comprehensive data analysis on Egyptian used car market data, utilizing advanced data preprocessing, statistical methods, and visualization techniques to extract meaningful insights.

---

## Data Preprocessing & Cleaning Methods

### 1. **Data Quality Assessment**
- Duplicate removal
- Identification and removal of illogical data (e.g., Year = 2026, Year = 0)
- Data type conversion and validation

### 2. **Data Extraction & Transformation**
- **Regular Expression Processing**: Extract numeric values from string-formatted numbers (e.g., "63,000" → 63000)
- **Shifting Data Correction**: Fix misaligned data across Transmission, Milage, Color, and Location columns
- **String Normalization**: Remove extra spaces and standardize formatting

### 3. **Missing Value Imputation**
- **Mean Imputation by Group**: Fill missing Milage values with year-specific mean values
- **Logical Constraints Handling**: Replace zero values with brand-year group means
- **Outlier-based Replacement**: Fill Milage values < 10,000 (pre-2024) with corresponding brand-year averages
- **Brand Aggregation**: Replace abnormally low prices (< 100,000 EGP) with brand-level mean prices

### 4. **Outlier Detection & Treatment**
- **Interquartile Range (IQR) Method**:
  - Calculate Q1 (25th percentile) and Q3 (75th percentile)
  - Compute IQR = Q3 - Q1
  - Define bounds: Lower = Q1 - 1.5×IQR, Upper = Q3 + 1.5×IQR
  - Remove observations outside these bounds
- Applied to: Year, Milage, and Price columns

### 5. **Categorical Data Normalization**
- Arabic text reshaping using `arabic_reshaper` library
- Bidirectional text handling for proper Arabic display
- Standardization of categorical values (Brand, Model, Location, Transmission, Color, Fuel)

---

## Statistical Analysis Methods

### 1. **Correlation Analysis**
- **Pearson Correlation Coefficient**: Calculate linear relationships between numeric variables (Year, Milage, Price)
- **Heatmap Visualization**: Display correlation matrix with formatted coefficients
- Identifies strength and direction of relationships between features

### 2. **Descriptive Statistics**
- Mean calculation by groups (Year, Brand)
- Quantile-based analysis (25th, 50th, 75th percentiles)
- Distribution analysis for Price, Milage, and Year

### 3. **Distribution Analysis**
- **Histogram with Kernel Density Estimation (KDE)**: Visualize continuous variable distributions
- Assess normality and skewness of Price, Milage, and Year
- Data comparison before and after outlier removal

### 4. **Comparative Analysis**
- **Line Plots**: Temporal trends showing Year vs Price and Year vs Milage relationships
- **Categorical Comparison**: 
  - Pie charts for Transmission type distribution
  - Violin plots for Price distribution by Fuel type
  - Bar plots for mean prices by Brand, Location, and Model

### 5. **Grouping & Aggregation**
- **Group-by Analysis**:
  - Average Milage by Brand and Year
  - Mean Price by Brand
  - Count aggregations for categorical variables
- **Sorting & Ranking**: Identify top 10 brands, locations, and models by price
- **Frequency Analysis**: Most purchased brands and popular car colors

---

## Data Visualization Techniques

### 1. **Univariate Analysis**
- Distribution plots with KDE curves
- Histograms for frequency distributions
- Bar charts for categorical frequencies

### 2. **Bivariate Analysis**
- Scatter plots with regression lines
- Line plots for temporal relationships
- Violin plots for categorical-numeric relationships
- Heatmaps for correlation matrices

### 3. **Multivariate Analysis**
- Subplots comparing multiple relationships simultaneously
- Top-N filtered visualizations
- Color-coded categorical groupings

### 4. **Categorical Visualization**
- Pie charts with percentage labels
- Stacked bar charts
- Grouped bar plots with multiple dimensions

---

## Data Workflow & Pipeline

### Stage 1: Data Loading
- Read Excel file containing raw car market data
- Initial data inspection and structure verification

### Stage 2: Data Cleaning
```
Raw Data → Remove Illogical Data → Remove Duplicates → Extract Integers → 
Fix Shifted Data → Fill Missing Values → Handle Zero Values → 
Address Low Mileage → Adjust Abnormal Prices → Data Ready
```

### Stage 3: Outlier Handling
- **With Outliers Dataset**: Original cleaned data
- **Without Outliers Dataset**: IQR-filtered data for robust analysis

### Stage 4: Arabic Text Processing
- Reshape Arabic text for proper display
- Apply bidirectional text handling
- Normalize all categorical columns

### Stage 5: Statistical Analysis & Visualization
- Calculate correlations
- Generate distribution plots
- Create comparative visualizations
- Produce summary statistics

---

## Statistical Measures Calculated

| Measure | Description | Applied To |
|---------|-------------|-----------|
| **Mean** | Average value | Milage (by Year/Brand), Price (by Brand) |
| **Median** | 50th percentile | Implicit in distribution analysis |
| **Q1, Q3** | 25th and 75th percentiles | Outlier detection (IQR method) |
| **IQR** | Interquartile range | Outlier boundary calculation |
| **Correlation (r)** | Linear relationship strength | Year-Price, Milage-Price |
| **Count** | Frequency aggregation | Brand distribution, Transmission types |
| **Standard Deviation** | Implicit in visualizations | Distribution shape analysis |

---

## Datasets Generated

1. **Data with Outliers** (df_4): Complete cleaned dataset maintaining all observations
2. **Data without Outliers** (df_5): Filtered dataset using IQR method
3. **Group Aggregations**: Brand-Year means, Location-Price means, etc.

---

## Tools & Libraries Used

- **Data Processing**: Pandas, NumPy
- **Visualization**: Seaborn, Matplotlib
- **Text Processing**: arabic_reshaper, python-bidi
- **Pattern Matching**: Regular Expressions (re)

---

## Key Project Insights

### Data Characteristics
- Multiple car brands with varying price ranges
- Mileage varies significantly by vehicle age
- Transmission types: Automatic, Manual, DSG
- Geographic distribution across Egyptian locations
- Fuel types: Petrol, Diesel, Hybrid, Electric

### Analysis Outputs
- Correlation matrices showing relationships
- Distribution comparisons (with/without outliers)
- Top-performing brands and locations by price
- Market segmentation by transmission type and fuel
- Temporal trends in car pricing and condition

---

## Quality Assurance Measures

✓ Duplicate detection and removal  
✓ IQR-based outlier identification  
✓ Data type validation  
✓ Missing value tracking and imputation  
✓ Logical constraint verification  
✓ Comparative analysis (before/after cleaning)  
✓ Visual validation through distribution plots  

---

## Project Structure

```
Egyptian-Cars-Analysis/
├── Main.ipynb                      # Primary analysis notebook
├── Preprocessing.ipynb             # Data cleaning workflow
├── Methods.py                      # Data preprocessing class
├── Visualizations.py              # Visualization methods class
├── DataSetScraping3.xlsx          # Raw dataset
├── Data_with_outliers.xlsx        # Processed data (all observations)
├── Data_without_outliers.xlsx     # Processed data (IQR filtered)
└── readme.md                       # Documentation
```

---

**Last Updated**: 2025-05-28  
**Data Language**: Arabic (Egyptian Arabic)  
**Analysis Scope**: Egyptian Used Car Market
