"""
Sistema de Orquestração de Testes
==================================

Gerencia execução inteligente de testes com otimização de recursos e análise de performance.
"""

import sys
import json
import time
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from enum import Enum
import subprocess


class TestCategory(Enum):
    """Categorias de testes"""
    UNIT = "unit"
    INTEGRATION = "integration"
    E2E = "e2e"
    ALL = "all"


class ExecutionMode(Enum):
    """Modos de execução"""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    CONDITIONAL = "conditional"
    OPTIMIZED = "optimized"


@dataclass
class TestExecutionConfig:
    """Configuração de execução de testes"""
    category: TestCategory
    mode: ExecutionMode
    workers: int = -1  # -1 = auto
    timeout: int = 300
    failfast: bool = False
    verbose: bool = True
    coverage: bool = True
    html_report: bool = True
    json_report: bool = True
    markers: Optional[List[str]] = None


@dataclass
class TestExecutionResult:
    """Resultado da execução de testes"""
    category: str
    mode: str
    total_tests: int
    passed: int
    failed: int
    skipped: int
    errors: int
    duration: float
    coverage_percentage: Optional[float] = None
    exit_code: int = 0


class TestOrchestrator:
    """
    Orquestrador de Testes Inteligente

    Gerencia execução de testes com:
    - Execução paralela otimizada
    - Análise de dependências
    - Monitoramento de recursos
    - Geração de relatórios
    """

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.tests_dir = project_root / "tests"
        self.results: List[TestExecutionResult] = []

    def build_pytest_command(self, config: TestExecutionConfig) -> List[str]:
        """
        Constrói comando pytest baseado na configuração

        Args:
            config: Configuração de execução

        Returns:
            Lista com comando e argumentos
        """
        cmd = ["pytest"]

        # Diretório de testes baseado na categoria
        if config.category == TestCategory.UNIT:
            cmd.append(str(self.tests_dir / "unit"))
        elif config.category == TestCategory.INTEGRATION:
            cmd.append(str(self.tests_dir / "integration"))
        elif config.category == TestCategory.E2E:
            cmd.append(str(self.tests_dir / "e2e"))
        else:
            cmd.append(str(self.tests_dir))

        # Execução paralela
        if config.mode in [ExecutionMode.PARALLEL, ExecutionMode.OPTIMIZED]:
            if config.workers == -1:
                cmd.extend(["-n", "auto"])
            else:
                cmd.extend(["-n", str(config.workers)])

        # Verbose
        if config.verbose:
            cmd.append("-v")

        # Coverage
        if config.coverage:
            cmd.extend([
                "--cov=tools",
                "--cov=ui",
                "--cov-report=term-missing",
                "--cov-report=html",
                "--cov-report=json",
            ])

        # Fail fast
        if config.failfast:
            cmd.append("-x")

        # Timeout
        cmd.extend(["--timeout", str(config.timeout)])

        # HTML Report
        if config.html_report:
            cmd.extend([
                "--html=htmlcov/pytest_report.html",
                "--self-contained-html"
            ])

        # JSON Report
        if config.json_report:
            cmd.extend([
                "--json-report",
                "--json-report-file=htmlcov/pytest_report.json"
            ])

        # Marcadores customizados
        if config.markers:
            for marker in config.markers:
                cmd.extend(["-m", marker])

        return cmd

    def execute_tests(self, config: TestExecutionConfig) -> TestExecutionResult:
        """
        Executa testes com a configuração especificada

        Args:
            config: Configuração de execução

        Returns:
            Resultado da execução
        """
        print(f"\n{'=' * 80}")
        print(f"🧪 Executando testes: {config.category.value}")
        print(f"⚙️  Modo: {config.mode.value}")
        print(f"{'=' * 80}\n")

        cmd = self.build_pytest_command(config)
        print(f"📝 Comando: {' '.join(cmd)}\n")

        start_time = time.time()

        try:
            result = subprocess.run(
                cmd,
                cwd=str(self.project_root),
                capture_output=False,
                text=True
            )
            exit_code = result.returncode
        except Exception as e:
            print(f"❌ Erro ao executar testes: {e}")
            exit_code = 1

        duration = time.time() - start_time

        # Analisa resultados do JSON report
        test_result = self._parse_results(config, duration, exit_code)

        self.results.append(test_result)
        return test_result

    def _parse_results(
        self,
        config: TestExecutionConfig,
        duration: float,
        exit_code: int
    ) -> TestExecutionResult:
        """
        Analisa resultados dos testes

        Args:
            config: Configuração de execução
            duration: Duração da execução
            exit_code: Código de saída

        Returns:
            Resultado estruturado
        """
        # Tenta ler o relatório JSON
        json_report_path = self.project_root / "htmlcov" / "pytest_report.json"
        coverage_json_path = self.project_root / "coverage.json"

        total_tests = 0
        passed = 0
        failed = 0
        skipped = 0
        errors = 0
        coverage_percentage = None

        if json_report_path.exists():
            try:
                with open(json_report_path) as f:
                    report = json.load(f)
                    summary = report.get("summary", {})
                    total_tests = summary.get("total", 0)
                    passed = summary.get("passed", 0)
                    failed = summary.get("failed", 0)
                    skipped = summary.get("skipped", 0)
            except Exception as e:
                print(f"⚠️ Erro ao ler relatório JSON: {e}")

        if coverage_json_path.exists() and config.coverage:
            try:
                with open(coverage_json_path) as f:
                    coverage = json.load(f)
                    coverage_percentage = coverage.get("totals", {}).get("percent_covered")
            except Exception as e:
                print(f"⚠️ Erro ao ler cobertura: {e}")

        return TestExecutionResult(
            category=config.category.value,
            mode=config.mode.value,
            total_tests=total_tests,
            passed=passed,
            failed=failed,
            skipped=skipped,
            errors=errors,
            duration=duration,
            coverage_percentage=coverage_percentage,
            exit_code=exit_code
        )

    def execute_pipeline(
        self,
        mode: ExecutionMode = ExecutionMode.OPTIMIZED
    ) -> List[TestExecutionResult]:
        """
        Executa pipeline completo de testes

        Args:
            mode: Modo de execução

        Returns:
            Lista de resultados
        """
        print("\n" + "=" * 80)
        print("🚀 INICIANDO PIPELINE DE TESTES")
        print("=" * 80)

        # Execução condicional: testes rápidos primeiro
        if mode == ExecutionMode.CONDITIONAL:
            # 1. Testes unitários rápidos
            unit_config = TestExecutionConfig(
                category=TestCategory.UNIT,
                mode=ExecutionMode.PARALLEL,
                markers=["unit and fast"],
                failfast=True
            )
            unit_result = self.execute_tests(unit_config)

            # Se testes unitários passarem, executa integração
            if unit_result.exit_code == 0:
                integration_config = TestExecutionConfig(
                    category=TestCategory.INTEGRATION,
                    mode=ExecutionMode.PARALLEL,
                    markers=["integration"]
                )
                self.execute_tests(integration_config)
            else:
                print("\n⚠️ Testes unitários falharam. Pulando testes de integração.")

        # Execução otimizada: paralelo com categorização
        elif mode == ExecutionMode.OPTIMIZED:
            # Testes unitários em paralelo
            unit_config = TestExecutionConfig(
                category=TestCategory.UNIT,
                mode=ExecutionMode.PARALLEL,
                workers=-1
            )
            self.execute_tests(unit_config)

            # Testes de integração em paralelo (menos workers por serem I/O bound)
            integration_config = TestExecutionConfig(
                category=TestCategory.INTEGRATION,
                mode=ExecutionMode.PARALLEL,
                workers=4
            )
            self.execute_tests(integration_config)

        # Execução sequencial
        elif mode == ExecutionMode.SEQUENTIAL:
            for category in [TestCategory.UNIT, TestCategory.INTEGRATION]:
                config = TestExecutionConfig(
                    category=category,
                    mode=ExecutionMode.SEQUENTIAL
                )
                self.execute_tests(config)

        # Execução paralela de tudo
        else:
            config = TestExecutionConfig(
                category=TestCategory.ALL,
                mode=ExecutionMode.PARALLEL
            )
            self.execute_tests(config)

        return self.results

    def generate_summary_report(self):
        """Gera relatório resumido da execução"""
        print("\n" + "=" * 80)
        print("📊 RELATÓRIO FINAL DE EXECUÇÃO")
        print("=" * 80 + "\n")

        total_duration = sum(r.duration for r in self.results)
        total_tests = sum(r.total_tests for r in self.results)
        total_passed = sum(r.passed for r in self.results)
        total_failed = sum(r.failed for r in self.results)
        total_skipped = sum(r.skipped for r in self.results)

        for result in self.results:
            status = "✅ PASSOU" if result.exit_code == 0 else "❌ FALHOU"
            print(f"\n{status} - {result.category.upper()}")
            print(f"  Testes: {result.total_tests} | "
                  f"✅ {result.passed} | "
                  f"❌ {result.failed} | "
                  f"⏭️ {result.skipped}")
            print(f"  Duração: {result.duration:.2f}s")
            if result.coverage_percentage:
                print(f"  Cobertura: {result.coverage_percentage:.2f}%")

        print("\n" + "=" * 80)
        print(f"🎯 TOTAL: {total_tests} testes em {total_duration:.2f}s")
        print(f"✅ Passed: {total_passed}")
        print(f"❌ Failed: {total_failed}")
        print(f"⏭️ Skipped: {total_skipped}")

        success_rate = (total_passed / total_tests * 100) if total_tests > 0 else 0
        print(f"📈 Taxa de Sucesso: {success_rate:.1f}%")
        print("=" * 80 + "\n")

        # Salva relatório em JSON
        report_path = self.project_root / "htmlcov" / "orchestration_report.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)

        with open(report_path, 'w') as f:
            json.dump(
                {
                    "summary": {
                        "total_duration": total_duration,
                        "total_tests": total_tests,
                        "total_passed": total_passed,
                        "total_failed": total_failed,
                        "total_skipped": total_skipped,
                        "success_rate": success_rate
                    },
                    "results": [asdict(r) for r in self.results]
                },
                f,
                indent=2
            )

        print(f"💾 Relatório salvo em: {report_path}")


def main():
    """Função principal"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Sistema de Orquestração de Testes OSINTLAB"
    )
    parser.add_argument(
        "--mode",
        choices=["sequential", "parallel", "conditional", "optimized"],
        default="optimized",
        help="Modo de execução (padrão: optimized)"
    )
    parser.add_argument(
        "--category",
        choices=["unit", "integration", "e2e", "all"],
        help="Categoria específica de testes"
    )

    args = parser.parse_args()

    project_root = Path(__file__).parent.parent
    orchestrator = TestOrchestrator(project_root)

    mode = ExecutionMode(args.mode)

    if args.category:
        # Executa apenas categoria específica
        category = TestCategory(args.category)
        config = TestExecutionConfig(category=category, mode=mode)
        orchestrator.execute_tests(config)
    else:
        # Executa pipeline completo
        orchestrator.execute_pipeline(mode)

    orchestrator.generate_summary_report()

    # Exit code baseado nos resultados
    exit_code = max((r.exit_code for r in orchestrator.results), default=0)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
