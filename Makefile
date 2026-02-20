# ============================================================
# Jarbin_C_Coding_Style – Makefile
# ============================================================
# Usage:
#   make help
#   make install
# ============================================================

# ------------------------------------------------------------
# CONFIGURATION
# ------------------------------------------------------------

PYTHON              ?= python3
SHELL               := /bin/bash
SCRIPT_DIR          := scripts
PACKAGE_NAME        := Jarbin_C_Coding_Style
PACKAGE_NAME_SHORT  := JCCS

# Colors (safe for most terminals)
GREEN               := \033[0;32m
YELLOW              := \033[0;33m
RED                 := \033[0;31m
NC                  := \033[0m

# ------------------------------------------------------------
# DEFAULT TARGET
# ------------------------------------------------------------

.DEFAULT_GOAL := help

# ------------------------------------------------------------
# HELP
# ------------------------------------------------------------

help:
	@echo -e "$(GREEN)$(PACKAGE_NAME) ($(PACKAGE_NAME_SHORT))$(NC)"
	@echo -e "$(GREEN)Available commands:$(NC)"
	@echo ""
	@echo -e "\tmake/make help\t\tShow this help message"
	@echo ""
	@echo -e "\tmake install\t\tInstall the package"
	@echo -e "\tmake uninstall\t\tUninstall the package"
	@echo -e "\tmake reinstall\t\tReinstall the package"
	@echo ""

# ------------------------------------------------------------
# PACKAGE MANAGEMENT
# ------------------------------------------------------------

install:
	@echo -e "$(YELLOW) [INSTALL] Installing $(PACKAGE_NAME_SHORT)$(NC)"
	@./$(SCRIPT_DIR)/install-jccs
	@echo -e "$(GREEN) [INSTALL] $(PACKAGE_NAME_SHORT) installed$(NC)"

uninstall:
	@echo -e "$(YELLOW) [UNINSTALL] Uninstalling $(PACKAGE_NAME_SHORT)$(NC)"
	@./$(SCRIPT_DIR)/uninstall-jccs
	@echo -e "$(GREEN) [UNINSTALL] $(PACKAGE_NAME_SHORT) uninstalled$(NC)"

reinstall:
	@echo -e "$(YELLOW) [REINSTALL] Reinstalling $(PACKAGE_NAME_SHORT)$(NC)"
	@make -s uninstall install
	@echo -e "$(GREEN) [REINSTALL] $(PACKAGE_NAME_SHORT) reinstalled$(NC)"

# ------------------------------------------------------------
# SAFETY
# ------------------------------------------------------------

.PHONY: \
	help \
	install uninstall reinstall