import os

import launch
from multi_threading.modules import cmd_args, script_loading
from multi_threading.modules.paths_internal import extensions_dir, extensions_builtin_dir

parser = cmd_args.parser

script_loading.preload_extensions(extensions_dir, parser, extension_list=launch.list_extensions(launch.args.ui_settings_file))
script_loading.preload_extensions(extensions_builtin_dir, parser)

if os.environ.get('IGNORE_CMD_ARGS_ERRORS', None) is None:
    cmd_opts = parser.parse_args()
else:
    cmd_opts, _ = parser.parse_known_args()

cmd_opts.webui_is_non_local = any([cmd_opts.share, cmd_opts.listen, cmd_opts.ngrok, cmd_opts.server_name])
cmd_opts.disable_extension_access = cmd_opts.webui_is_non_local and not cmd_opts.enable_insecure_extension_access
