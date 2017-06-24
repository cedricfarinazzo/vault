#!/usr/bin/env python3

import os

import argparse

from lib.Vault import Vault
from lib.Config import Config
from lib.ImportExport import ImportExport
from lib.Misc import *

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--clipboard_TTL", type=int, help="Set clipboard TTL (in seconds, default: 15)", nargs='?', const = 15)
parser.add_argument("-a", "--auto_lock_TTL", type=int, help="Set auto lock TTL (in seconds, default: 900)", nargs='?', const = 900)
parser.add_argument("-v", "--vault_location", type=str, help="Set vault path")
parser.add_argument("-c", "--config_location", type=str, help="Set config path")
parser.add_argument("-k", "--change_key", action='store_true', help="Change master key")
parser.add_argument("-i", "--import_items", type=str, help="File to import credentials from")
parser.add_argument("-x", "--export", type=str, help="File to export credentials to")
parser.add_argument("-e", "--erase_vault", action='store_true', help="Erase the vault and config file")
args = parser.parse_args()

# Default paths
ConfigPathDefault = os.path.expanduser('~') + '/.vault_config'
vaultPathDefault = os.path.expanduser('~') + '/.vault_secure'

def getVaultPath():
    """
        Returns the vault location (either default or user defined)
    """

    global args, vaultPathDefault

    if args.vault_location:
        return args.vault_location;
    return vaultPathDefault;

def getConfigPath():
    """
        Returns the config location (either default or user defined)
    """

    global args, ConfigPathDefault

    if args.config_location:
        return args.config_location;
    return ConfigPathDefault;

if __name__ == '__main__':
    # Some nice ascii art
    logo()

    # Assess files integrity
    assessIntegrity(getVaultPath(), getConfigPath())

    # Erase a vault if the user requests it
    if args.erase_vault:
        eraseVault(getVaultPath(), getConfigPath())

    # Load config
    c = Config(getConfigPath())
    config = c.getConfig()

    # Update config
    if args.clipboard_TTL:
        c.update('clipboardTTL', args.clipboard_TTL)
    elif args.auto_lock_TTL:
        c.update('autoLockTTL', args.auto_lock_TTL)

    # Init Vault
    v = Vault(config, getVaultPath())

    # Change vault key
    if args.change_key:
        v.changeKey()

    # Import items to the vault
    if args.import_items:
        print()
        print("Please consider backing up your vault located at `%s` before proceeding." % (getVaultPath()));
        print()
        ie = ImportExport(v)
        ie.importItems(args.import_items)

    # Export vault
    if args.export:
        ie = ImportExport(v)
        ie.export(args.export)

    # Check if the vault exists
    if not os.path.isfile(getVaultPath()):
        v.setup()
    # Offer to unlock the vault
    else:
        v.unlock()
