# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 18:31:00 2022

@author: Pedro Sader Azevedo
"""
import matplotlib.pyplot as plt
import pandas as pd
import os
from typing import List

DATA_DIR = "data"
IMG_DIR = "img"
DPI = 600


def main() -> None:
    analyze_data()


def analyze_data():
    filenames = os.listdir(os.path.join(DATA_DIR, "raw"))
    for f in filenames:
        df: pd.DataFrame = pd.read_excel(os.path.join(DATA_DIR, "raw", f))
        df.rename(
            columns={
                "Frequência (Hz)": "f",
                "Tensão de entrada (V)": "V1",
                "Menor divisão da entrada (V)": "mindiv1",
                "Tensão de saída (V)": "V2",
                "Menor divisão da saída (V)": "mindiv2",
                "Diferença de fase (s)": "phi",
                "Menor divisão da fase (s)": "mindiv_phi",
                "Capacitância (F)": "C",
                "Frequência de corte teórica (Hz)": "fc",
            },
            inplace=True,
        )

        df["V2V1"] = df["V2"] / df["V1"]
        df["u_V1"] = voltage_uncertainty(df["V1"], df["mindiv1"])
        df["u_V2"] = voltage_uncertainty(df["V2"], df["mindiv2"])
        df["u_V2V1"] = ratio_uncertainty(df["V2"], df["u_V2"], df["V1"], df["u_V1"])

        if "parte01" in f:
            analyze_data_part01(df)
        elif "parte02" in f:
            analyze_data_part02(df)


def rectangular(a: float) -> float:
    return a / (2 * 3 ** (1 / 2))


def triangular(a: float) -> float:
    return a / (2 * 6 ** (1 / 2))


def combine(uncertainties: List[float]):
    acc = 0
    for u in uncertainties:
        acc += u**2
    return acc ** (1 / 2)


def voltage_uncertainty(voltage: float, mindiv: float):
    u_calibration = rectangular(0.03 * voltage + 0.1 * mindiv + 0.001)
    u_reading = rectangular(mindiv)
    return combine([u_calibration, u_reading])


def phase_uncertainty(phase: float, mindiv: float):
    u_peak = triangular(0.1 * phase)
    u_reading = rectangular(mindiv)
    return combine([u_peak, u_reading])


def ratio_uncertainty(a: float, u_a: float, b: float, u_b: float):
    return ((1 / b**2) * (u_a + (a**2 * u_b) / b**2)) ** (1 / 2)


def analyze_data_part01(df: pd.DataFrame):
    df["u_phi"] = phase_uncertainty(df["phi"], df["mindiv_phi"])

    # gráfico de razão de tensões
    _, ax1 = plt.subplots(1, 1)
    ax1.errorbar(
        x=df["f"],
        y=df["V2V1"],
        yerr=df["u_V2V1"],
        fmt="o",
        elinewidth=1,
        capsize=3,
        capthick=1,
        ms=3,
        c="blue",
        ecolor="black",
    )
    ax1.set_xscale("log")
    ax1.set_title("Razão entre Tensões de Saída e Entrada por Frequência (Hz)")
    ax1.set_xlabel("Frequência (HZ)")
    ax1.set_ylabel("V2/V1")
    plt.tight_layout()
    plt.savefig(os.path.join(IMG_DIR, "plots", "part01_V2V1.png"), dpi=DPI)

    # gráfico de diferença de fase
    _, ax2 = plt.subplots(1, 1)
    ax2.errorbar(
        x=df["f"],
        y=df["phi"],
        yerr=df["u_phi"],
        fmt="o",
        elinewidth=1,
        capsize=3,
        capthick=1,
        ms=3,
        c="red",
        ecolor="black",
    )
    ax2.set_xscale("log")
    ax2.set_title("Diferença de Fase (s) por Frequência (Hz)")
    ax2.set_xlabel("Frequência (HZ)")
    ax2.set_ylabel("Diferença de Fase (s)")
    plt.tight_layout()
    plt.savefig(os.path.join("plots", "part01_phi.png"), dpi=DPI)

    # salvar tabela alterada
    df["f (Hz)"] = df["f"]
    df["V1 (V)"] = df["V1"].apply(str) + " ± " + df["u_V1"].round(3).apply(str)
    df["V2 (V)"] = df["V2"].apply(str) + " ± " + df["u_V2"].round(3).apply(str)
    df["V2/V1"] = (
        df["V2V1"].round(3).apply(str) + " ± " + df["u_V2V1"].round(3).apply(str)
    )
    df["ɸ (s)"] = df["V2"].apply(str) + " ± " + df["u_V2"].round(3).apply(str)
    df = df.iloc[:, -5:]
    df.to_csv(os.path.join(DATA_DIR, "clean", "parte01.csv"))


def analyze_data_part02(df: pd.DataFrame):
    # gráfico de razão de tensões
    _, ax = plt.subplots(1, 1)
    ax.errorbar(
        x=df["C"],
        y=df["V2V1"],
        yerr=df["u_V2V1"],
        fmt="o",
        elinewidth=1,
        capsize=3,
        capthick=1,
        ms=3,
        c="green",
        ecolor="black",
        label="Experimental",
    )
    ax.axhline(y=0.7, color="green", alpha=0.5, linestyle="--", label="Teórico")
    ax.set_title("Razão entre Tensões de Entrada e Saída por Capacitância (F)")
    ax.set_xlabel("Capacitância (F)")
    ax.set_ylabel("V2V1")
    ax.set_ylim([0.5, 0.9])
    ax.legend(loc="best")
    plt.tight_layout()
    plt.savefig(os.path.join("plots", "part02_V2V1.png"), dpi=DPI)

    # salvar tabela alterada
    df["f (Hz)"] = df["fc"]
    df["V1 (V)"] = df["V1"].apply(str) + " ± " + df["u_V1"].round(3).apply(str)
    df["V2 (V)"] = df["V2"].apply(str) + " ± " + df["u_V2"].round(3).apply(str)
    df["V2/V1"] = df["V2V1"].apply(str) + " ± " + df["u_V2V1"].round(3).apply(str)
    df = df.iloc[:, -4:]
    df.to_csv(os.path.join(DATA_DIR, "clean", "parte02.csv"))


if __name__ == "__main__":
    main()