# exploratory_analysis.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from tabulate import tabulate

class ExploratoryAnalysis:
    def __init__(self, df, image_dir="eda_images"):
        self.df = df
        self.image_dir = image_dir
        os.makedirs(image_dir, exist_ok=True)

    def describir_tipos_datos(self):
        """
        Describe los tipos de datos presentes en el DataFrame de forma legible.

        Returns:
        list: Una lista de descripciones legibles por tipo de dato.
        """
        descripciones = {
            'object': 'variables categóricas o de texto',
            'float64': 'variables numéricas decimales (float64)',
            'int64': 'variables numéricas enteras',
            'bool': 'variables booleanas (True/False)',
            'datetime64[ns]': 'variables de fecha y hora'
        }

        conteo = self.df.dtypes.value_counts()
        resultado = []

        for tipo, cantidad in conteo.items():
            descripcion = descripciones.get(str(tipo), f'variables de tipo {tipo}')
            resultado.append(f"Tenemos {cantidad} {descripcion}.")

        return resultado
    
    def dataframe_a_imagen(self,df, path='tabla.png', max_filas=5):
        tabla = df.head(max_filas)

        fig, ax = plt.subplots(figsize=(tabla.shape[1]*1.8, max_filas*0.6))
        ax.axis('tight')
        ax.axis('off')

        # Crear tabla visual
        tabla_plot = ax.table(
            cellText=tabla.values,
            colLabels=tabla.columns,
            cellLoc='center',
            loc='center'
        )

        tabla_plot.auto_set_font_size(False)
        tabla_plot.set_fontsize(10)
        tabla_plot.scale(1, 1.5)  # ajustar tamaño

        plt.savefig(path, bbox_inches='tight', dpi=300)
        plt.close()
        return path
    
    def get_basic_info(self):
        num_filas, num_columnas = self.df.shape
        tipos = self.df.dtypes
        num_decimales = sum(t.name == "float64" for t in tipos)
        num_categoricos = sum(t.name == "object" for t in tipos)

        fila_txt = "fila" if num_filas == 1 else "filas"
        col_txt = "columna" if num_columnas == 1 else "columnas"
        dec_txt = "es" if num_decimales == 1 else "son"
        cat_txt = "es" if num_categoricos == 1 else "son"

        info += f"El dataset contiene {num_filas} {fila_txt} y {num_columnas} {col_txt}, "
        info += f"de las cuales {num_decimales} {dec_txt} numéricas decimales (float64) "
        info += f"y {num_categoricos} {cat_txt} categóricas.\n\n"
        info += "A continuación se presentan las primeras filas del dataset:\n\n"
        info += dataframe_a_imagen(self,self.df, path="tabla.png")
        return info
    import matplotlib.pyplot as plt


    def get_null_summary(self):
        nulls = self.df.isnull().sum()
        return nulls[nulls > 0]

    def save_describe_table(self, path):
        self.df.describe().to_csv(path)

    def plot_histograms(self, max_plots=3):
        num_cols = self.df.select_dtypes(include='number').columns[:max_plots]
        paths = []
        for col in num_cols:
            plt.figure(figsize=(5, 3))
            sns.histplot(self.df[col].dropna(), kde=True)
            plt.title(f"Distribución: {col}")
            img_path = os.path.join(self.image_dir, f"hist_{col}.png")
            plt.savefig(img_path)
            plt.close()
            paths.append(img_path)
        return paths

    def plot_boxplots(self, max_plots=3):
        num_cols = self.df.select_dtypes(include='number').columns[:max_plots]
        paths = []
        for col in num_cols:
            plt.figure(figsize=(5, 3))
            sns.boxplot(x=self.df[col])
            plt.title(f"Boxplot: {col}")
            img_path = os.path.join(self.image_dir, f"box_{col}.png")
            plt.savefig(img_path)
            plt.close()
            paths.append(img_path)
        return paths

    def plot_pairplot(self, max_vars=5):
        num_cols = self.df.select_dtypes(include='number').columns[:max_vars]
        if len(num_cols) > 1:
            pairplot_path = os.path.join(self.image_dir, "pairplot.png")
            sns.pairplot(self.df[num_cols])
            plt.savefig(pairplot_path, bbox_inches="tight")
            plt.close()
            return pairplot_path
        else:
            return None

    def plot_correlation_heatmap(self):
        corr = self.df.corr(numeric_only=True)
        plt.figure(figsize=(6, 4))
        sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
        heatmap_path = os.path.join(self.image_dir, "corr_heatmap.png")
        plt.savefig(heatmap_path, bbox_inches="tight")
        plt.close()
        return heatmap_path

    def plot_categorical_counts(self, max_plots=3):
        cat_cols = self.df.select_dtypes(include='object').columns[:max_plots]
        paths = []
        for col in cat_cols:
            plt.figure(figsize=(5, 3))
            sns.countplot(y=self.df[col])
            plt.title(f"Conteo de categorías: {col}")
            img_path = os.path.join(self.image_dir, f"count_{col}.png")
            plt.savefig(img_path)
            plt.close()
            paths.append(img_path)
        return paths

    def plot_categorical_boxplots(self, max_plots=3):
        cat_cols = self.df.select_dtypes(include='object').columns[:max_plots]
        num_cols = self.df.select_dtypes(include='number').columns[:max_plots]
        paths = []
        for cat_col in cat_cols:
            for num_col in num_cols:
                plt.figure(figsize=(5, 3))
                sns.boxplot(x=self.df[cat_col], y=self.df[num_col])
                plt.title(f"Boxplot: {num_col} por {cat_col}")
                img_path = os.path.join(self.image_dir, f"box_{num_col}_by_{cat_col}.png")
                plt.savefig(img_path)
                plt.close()
                paths.append(img_path)
        return paths

    def plot_categorical_pairplot(self, max_vars=5):
        cat_cols = self.df.select_dtypes(include='object').columns[:max_vars]
        if len(cat_cols) > 1:
            pairplot_path = os.path.join(self.image_dir, "cat_pairplot.png")
            sns.pairplot(self.df[cat_cols])
            plt.savefig(pairplot_path, bbox_inches="tight")
            plt.close()
            return pairplot_path
        else:
            return None

    def plot_all(self):
        all_paths = []
        all_paths.extend(self.plot_histograms())
        all_paths.extend(self.plot_boxplots())
        corr_path = self.plot_correlation_heatmap()
        if corr_path:
            all_paths.append(corr_path)
        pairplot_path = self.plot_pairplot()
        if pairplot_path:
            all_paths.append(pairplot_path)
        all_paths.extend(self.plot_categorical_counts())
        all_paths.extend(self.plot_categorical_boxplots())
        cat_pairplot_path = self.plot_categorical_pairplot()
        if cat_pairplot_path:
            all_paths.append(cat_pairplot_path)
        return all_paths