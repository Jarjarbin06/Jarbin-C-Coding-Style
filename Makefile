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
	echo -e "$(GREEN)$(PACKAGE_NAME) ($(PACKAGE_NAME_SHORT))$(NC)"
	echo -e "$(GREEN)Available commands:$(NC)"
	echo ""
	echo -e "\tmake/make help\t\tShow this help message"
	echo ""
	echo -e "\tmake install\t\tInstall the package"
	echo -e "\tmake uninstall\t\tUninstall the package"
	echo -e "\tmake reinstall\t\tReinstall the package"
	echo ""
	echo -e "\tmake update\t\tUpdate the package"
	echo -e "\t\t\t\t(used by JCCS --update, do not launch it manually)"
	echo ""

# ------------------------------------------------------------
# PACKAGE MANAGEMENT
# ------------------------------------------------------------

install:
	echo -e "\t$(YELLOW)[INSTALL] Installing $(PACKAGE_NAME_SHORT)$(NC)\n"
	./$(SCRIPT_DIR)/install-jccs 2>/dev/null || (echo -e "\n\t$(RED)[INSTALL] $(PACKAGE_NAME_SHORT) failed to install$(NC)"; false)
	echo -e "\n\t$(GREEN)[INSTALL] $(PACKAGE_NAME_SHORT) installed$(NC)"

uninstall:
	echo -e "\t$(YELLOW)[UNINSTALL] Uninstalling $(PACKAGE_NAME_SHORT)$(NC)\n"
	./$(SCRIPT_DIR)/uninstall-jccs 2>/dev/null || (echo -e "\n\t$(RED)[UNINSTALL] $(PACKAGE_NAME_SHORT) failed to uninstall$(NC)"; false)
	echo -e "\n\t$(GREEN)[UNINSTALL] $(PACKAGE_NAME_SHORT) uninstalled$(NC)"

reinstall:
	echo -e "$(YELLOW) [REINSTALL] Uninstalling $(PACKAGE_NAME_SHORT)$(NC)\n"
	make -s uninstall 2>/dev/null || (echo -e "\n$(RED) [REINSTALL] $(PACKAGE_NAME_SHORT) failed to uninstall$(NC)"; false)
	echo -e "\n$(YELLOW) [REINSTALL] Reinstalling $(PACKAGE_NAME_SHORT)$(NC)\n"
	make -s install 2>/dev/null || (echo -e "\n$(RED) [REINSTALL] $(PACKAGE_NAME_SHORT) failed to reinstall$(NC)"; false)
	echo -e "\n$(GREEN) [REINSTALL] $(PACKAGE_NAME_SHORT) reinstalled$(NC)"

update:
	echo -e "$(YELLOW) [UPDATE] Updating $(PACKAGE_NAME_SHORT)$(NC)\n"
	git pull
	make -s reinstall
	echo -e "\n$(GREEN) [UPDATE] $(PACKAGE_NAME_SHORT) updated$(NC)"

# ------------------------------------------------------------
# SAFETY
# ------------------------------------------------------------

.SILENT: \
	help \
	install uninstall reinstall update

.PHONY: \
	help \
	install uninstall reinstall update