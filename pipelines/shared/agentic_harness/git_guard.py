import subprocess
from pathlib import Path

class GitGuard:
    """
    Gestiona checkpoints y rollbacks en Git durante ejecuciones agénticas
    para evitar pérdidas de código o corrupción del workspace.
    """
    def __init__(self):
        self.workspace_root = Path(__file__).resolve().parents[3]

    def _run_git(self, args: list) -> str:
        try:
            result = subprocess.run(
                ["git"] + args,
                cwd=str(self.workspace_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error ejecutando git {' '.join(args)}: {e.stderr.strip()}") from e

    def create_checkpoint(self, name: str) -> str:
        """Crea un commit temporal de respaldo."""
        # Verificar estado limpio o sucio
        status = self._run_git(["status", "--porcelain"])
        if not status:
            return "Workspace limpio. No se requiere checkpoint."
            
        self._run_git(["add", "."])
        commit_msg = f"[agent-checkpoint] {name}"
        output = self._run_git(["commit", "-m", commit_msg])
        return f"Checkpoint '{name}' creado con éxito: {output}"

    def rollback(self, name: str) -> str:
        """Revierte el workspace al estado del checkpoint especificado."""
        commit_msg = f"[agent-checkpoint] {name}"
        
        # Buscar el hash del commit por su mensaje
        log = self._run_git(["log", "--grep", commit_msg, "-n", "1", "--format=%H"])
        if not log:
            raise ValueError(f"No se encontró ningún checkpoint con el nombre: {name}")
            
        commit_hash = log.strip()
        
        # Hacer reset hard al commit anterior del checkpoint (o al checkpoint mismo si queremos volver a ese estado)
        # Queremos volver al estado del checkpoint, es decir, el commit del checkpoint:
        self._run_git(["reset", "--hard", commit_hash])
        
        # Deshacer el commit del checkpoint pero dejando los archivos en el estado del checkpoint,
        # o revertir el commit para que el workspace quede libre del commit temporal:
        self._run_git(["reset", "HEAD~1"])
        
        return f"Workspace revertido con éxito al estado de '{name}' (commit {commit_hash[:7]})"
        
    def discard_checkpoint(self, name: str) -> str:
        """Elimina el checkpoint de Git dejando los cambios en el directorio de trabajo."""
        commit_msg = f"[agent-checkpoint] {name}"
        log = self._run_git(["log", "--grep", commit_msg, "-n", "1", "--format=%H"])
        if not log:
            return "No se encontró el checkpoint para descartar."
            
        commit_hash = log.strip()
        self._run_git(["reset", "HEAD~1"])
        return f"Checkpoint Git descartado. Cambios preservados localmente."
