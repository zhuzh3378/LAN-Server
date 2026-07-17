import os
import socket
import http.server
import socketserver

# ================= 颜色配置 =================
# 使用 ANSI 转义序列实现控制台颜色，\033[92m 是亮绿色，\033[0m 是重置颜色
GREEN = '\033[92m'
RESET = '\033[0m'
# ============================================

def get_local_ip():
    """获取本机局域网IP地址"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def is_port_available(port):
    """检查指定端口是否可用"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("0.0.0.0", port))
            return True
        except OSError:
            return False

def get_valid_port(default_port):
    """获取可用的端口。如果默认端口被占用，则循环提示用户输入新端口"""
    port = default_port
    while True:
        if is_port_available(port):
            return port
        
        print(f"\n⚠️  端口 {port} 已被占用！")
        user_input = input("👉 请输入一个新的端口号 (1024-65535)，或输入 'q' 退出: ").strip()
        
        if user_input.lower() == 'q':
            print("✅ 已取消启动。")
            exit(0)
        
        try:
            new_port = int(user_input)
            if 1024 <= new_port <= 65535:
                port = new_port
            else:
                print("❌ 端口号必须在 1024 到 65535 之间，请重新输入。")
        except ValueError:
            print("❌ 输入无效，请输入纯数字。")

def main():
    # ================= 配置区 =================
    html_dir = "html"   # 存放网页文件的文件夹名称
    port = 8000         # 默认服务器端口
    # ==========================================

    # 1. 检查并创建 html 文件夹
    if not os.path.exists(html_dir):
        os.makedirs(html_dir)
        with open(os.path.join(html_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write("<!DOCTYPE html><html><head><meta charset='UTF-8'><title>服务器就绪</title></head>"
                    "<body style='font-family:sans-serif; text-align:center; margin-top:50px;'>"
                    "<h1>🚀 服务器启动成功！</h1>"
                    "<p>请将你的 HTML 文件放入 <code>html</code> 文件夹中。</p>"
                    "<p>如果是 index.html，刷新此页面即可看到。</p>"
                    "</body></html>")
        print(f"💡 未找到 '{html_dir}' 文件夹，已自动创建，并生成了默认的 index.html。")

    # 2. 获取本机局域网 IP
    local_ip = get_local_ip()

    # 3. 获取最终可用的端口（处理端口占用逻辑）
    final_port = get_valid_port(port)

    # 4. 切换到 html 目录
    original_dir = os.getcwd()
    os.chdir(html_dir)

    # 允许端口重用
    socketserver.TCPServer.allow_reuse_address = True

    try:
        # 5. 启动服务器
        with socketserver.TCPServer(("0.0.0.0", final_port), http.server.SimpleHTTPRequestHandler) as httpd:
            print("\n" + "=" * 60)
            print("🚀 局域网 HTTP 服务器已成功启动！")
            print(f"📂 网站根目录: {os.path.abspath(html_dir)}")
            print("-" * 60)
            
            # 【优化点1】：将 URL 部分高亮为绿色
            print(f"🖥️  本机访问地址: {GREEN}http://127.0.0.1:{final_port}{RESET}")
            print(f"📱 局域网访问地址: {GREEN}http://{local_ip}:{final_port}{RESET}")
            
            print("-" * 60)
            print("💡 提示: 请确保手机/其他设备与电脑连接在 同一个WiFi/局域网 下。")
            print("🛑 按 Ctrl+C 停止服务器...")
            print("=" * 60 + "\n")
            
            # 保持运行
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n\n✅ 服务器已手动停止。")
    except Exception as e:
        print(f"\n❌ 发生未知错误: {e}")
    finally:
        # 恢复原来的工作目录
        os.chdir(original_dir)

if __name__ == "__main__":
    main()