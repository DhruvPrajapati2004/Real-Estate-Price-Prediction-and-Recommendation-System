# Run your script as Administrator (otherwise it will fail with "operation requires elevation").
import subprocess
import time

def reset_wifi(adapter_name="Wi-Fi"):
    try:
        print("🔌 Disabling Wi-Fi...")
        subprocess.run([
            "powershell",
            f"Disable-NetAdapter -Name '{adapter_name}' -Confirm:$false"
        ], check=True)
        
        time.sleep(5)

        print("📶 Enabling Wi-Fi...")
        subprocess.run([
            "powershell",
            f"Enable-NetAdapter -Name '{adapter_name}' -Confirm:$false"
        ], check=True)

        print("✅ Wi-Fi reset successfully.")
        
    except subprocess.CalledProcessError as e:
        print("❌ Failed to reset Wi-Fi:", e)
