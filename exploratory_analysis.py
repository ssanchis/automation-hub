# exploratory_analysis.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

class ExploratoryAnalysis:
    def __init__(self, df, image_dir="eda_images"):
        self.df = df
        self.image_dir = image_dir
        os.makedirs(image_dir, exist_ok=True)

    def get_basic_info(self):
        info = f"Forma: {self.df.shape},tenemos {self.df.shape[1]} columnas y {self.df.shape[0]} filas.\n\nTipos de datos:\n{self.df.dtypes}\n\n"
        info += "Primeras filas:\n" + str(self.df.head()) + "\n\n"
        info += "Columnas:\n" + str(self.df.columns.tolist()) + "\n\n"
        info += "Tipos de datos únicos por columna:\n" + str(self.df.dtypes.value_counts()) + "\n\n"
        return info

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