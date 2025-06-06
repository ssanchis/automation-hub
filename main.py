# main.py
import pandas as pd
from exploratory_analysis import ExploratoryAnalysis
from pdf_report import PDFReport
import matplotlib.pyplot as plt
import os

# Ruta del dataset y nombre de salida
DATA_PATH = "iris.csv"
PDF_OUTPUT = "informe_eda.pdf"
IMAGE_DIR = "eda_images"

# Cargar los datos
def load_data(file_path):
        """
        Load the dataset from a file (CSV, Excel, JSON).

        Parameters:
        file_path (str): Path to the file.

        Returns:
        pd.DataFrame: Loaded dataset.

        Raises:
        ValueError: If the file type is unsupported or cannot be read.
        """
        ext = os.path.splitext(file_path)[1].lower()

        try:
            if ext == '.csv':
                return pd.read_csv(file_path)
            elif ext in ['.xls', '.xlsx']:
                return pd.read_excel(file_path)
            elif ext == '.json':
                return pd.read_json(file_path)
            else:
                raise ValueError(f"Unsupported file extension: '{ext}'. Supported types: .csv, .xlsx, .xls, .json")
        except Exception as e:
            raise ValueError(f"Error loading file '{file_path}': {e}")

df = load_data(DATA_PATH)

# Inicializar clase de análisis EDA
eda = ExploratoryAnalysis(df, image_dir=IMAGE_DIR)

# Inicializar el PDF
pdf = PDFReport()
pdf.add_page()

# 1. Info básica
pdf.chapter_title("1. Información general")
info = eda.get_basic_info()
pdf.chapter_body(info)

# 2. Valores nulos
pdf.chapter_title("2. Valores nulos")
nulls = eda.get_null_summary()
if not nulls.empty:
    pdf.chapter_body(str(nulls))
else:
    pdf.chapter_body("No hay valores nulos.")

# 3. Estadísticas descriptivas
desc_csv = os.path.join(IMAGE_DIR, "desc.csv")
desc_img = os.path.join(IMAGE_DIR, "describe.png")
eda.save_describe_table(desc_csv)
desc_df = pd.read_csv(desc_csv)
fig, ax = plt.subplots(figsize=(10, 4))
ax.axis("off")
ax.table(cellText=desc_df.values, colLabels=desc_df.columns, loc='center')
plt.savefig(desc_img, bbox_inches="tight")
plt.close()
pdf.chapter_title("3. Estadísticas descriptivas")
pdf.add_image(desc_img)

# 4. Histogramas
pdf.chapter_title("4. Distribuciones numéricas")
hist_paths = eda.plot_histograms()
for path in hist_paths:
    pdf.add_image(path)

# 5. Boxplots numéricos
pdf.chapter_title("5. Boxplots de variables numéricas")
box_paths = eda.plot_boxplots()
for path in box_paths:
    pdf.add_image(path)

# 6. Matriz de correlación
pdf.chapter_title("6. Matriz de correlación")
corr_path = eda.plot_correlation_heatmap()
if corr_path:
    pdf.add_image(corr_path)

# 7. Pairplot numérico
pdf.chapter_title("7. Pairplot de variables numéricas")
pairplot_path = eda.plot_pairplot()
if pairplot_path:
    pdf.add_image(pairplot_path)

# 8. Gráficos de categorías
pdf.chapter_title("8. Conteo de categorías")
cat_count_paths = eda.plot_categorical_counts()
for path in cat_count_paths:
    pdf.add_image(path)

# 9. Boxplots categóricos
pdf.chapter_title("9. Boxplots categórico-numéricos")
cat_box_paths = eda.plot_categorical_boxplots()
for path in cat_box_paths:
    pdf.add_image(path)

# 10. Pairplot categórico
pdf.chapter_title("10. Pairplot categórico")
cat_pairplot_path = eda.plot_categorical_pairplot()
if cat_pairplot_path:
    pdf.add_image(cat_pairplot_path)

# Guardar el PDF
pdf.output(PDF_OUTPUT)
print(f"PDF guardado como '{PDF_OUTPUT}'")
