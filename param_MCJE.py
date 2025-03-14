# Parameters for Minecraft Java Edition

from mc_remote.vec3 import Vec3
import mc_remote.block_1_21_4 as block
import mc_remote.entity_1_21_4 as entity
import mc_remote.particle_1_21_4 as particle

# PLAYER_NAME = "PLAYER_NAME"  # set your player name in Minecraft
PLAYER_NAME = "xxxx"  # set your player name in Minecraft
PLAYER_ORIGIN = Vec3(5000, 0, 5000)  # po.x, po.y, po.z
print(f"param_MCJE loaded for {PLAYER_NAME} at {PLAYER_ORIGIN.x}, {PLAYER_ORIGIN.y}, {PLAYER_ORIGIN.z}")

# minecraft remote connection to the host at address:port
ADRS_MCR = "localhost"  # Minecraft server running on your pc
# ADRS_MCR = "mc-remote.xgames.jp"  # mc-remote "Sandbox" server
PORT_MCR = 25575  # socket server port

# vertical levels in Minecraft 1.18+
Y_TOP = 320  # the top where blocks can be set
Y_CLOUD_BOTTOM = 199  # the bottom of clouds
Y_SEA = 62  # the sea level
Y_BOTTOM = 0  # the bottom where blocks can be set
Y_BOTTOM_STEVE = -64  # the bottom where Steve can go down

# For the block IDs and entity IDs, use the script get_block_id.py and get_entity_id.py to generate the list.
# Usage:
#     python mcje/get_block_id.py 1.21.4  # run the script in the terminal
#     python mcje/get_entity_id.py 1.21.4  # run the script in the terminal
#     You will get mcje/blocks_1_21_4.py containing all the block IDs for Minecraft 1.21.4.
#     You have to play Minecraft 1.21.4 at least once beforehand.
#
#     setBlock(x, y, z, block.GOLD_BLOCK)  # if you want to use the block ID in other files
#     spawnEntity(x, y, z, entity.CREEPER)  # if you want to use the entity ID in other files

block.GOLD_BLOCK  # if you want to use the block ID in this file
entity.CREEPER  # if you want to use the entity ID in this file
particle.HEART  # if you want to use the particle ID in this file
