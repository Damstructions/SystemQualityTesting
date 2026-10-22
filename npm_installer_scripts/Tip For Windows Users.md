# Tip For Windows Users

# Windows 用户说明

这份说明配合同目录下的 `Windows.ps1` 使用。脚本会先检查本机是否已经有 npm。若能找到，它会打印当前版本并结束。若找不到，它会通过 Windows 包管理器 winget 静默安装 Node.js LTS（包标识为 `OpenJS.NodeJS.LTS`），并在结束时提示你新开一个 PowerShell 窗口，再运行 `npm --version`。

This note belongs with `Windows.ps1` in the same folder. The script checks whether npm is already available. When npm is found, it prints the version and exits. When npm is missing, it silently installs Node.js LTS through winget (package id `OpenJS.NodeJS.LTS`), then asks you to open a new PowerShell window and run `npm --version`.

客户常见的反馈是：在完成某一项 Windows 设置之前，这个 `.ps1` 根本无法启动。该项设置是 PowerShell 的**执行策略（Execution Policy）**。Windows 客户端出厂默认值为 `Restricted`。在这个策略下，系统拒绝运行任何 PowerShell 脚本，终端里通常会出现下面这句：

Customers often report that the `.ps1` file will not start until a Windows setting is completed. That setting is the PowerShell **execution policy**. On a Windows client the factory default is `Restricted`. Under that policy Windows refuses to run PowerShell scripts, and the terminal usually shows:

```text
... cannot be loaded because running scripts is disabled on this system.
```

中文环境里，同一含义常显示为“在此系统上禁止运行脚本”。脚本内容还没有开始执行，所以这不是 npm 或 winget 的故障。

On a Chinese-language system the same message usually says that running scripts is disabled on this system. The script body has not started yet, so this is not an npm or winget failure.

## 在 Windows 设置里打开它

## Turn it on in Windows Settings

这项开关会把**当前用户**的执行策略改为 `RemoteSigned`。改完之后，本机上编写或复制来的脚本可以运行；从浏览器、邮件或聊天软件下载的脚本，仍需要受信任的数字签名，或者先按下一节解除锁定。开关立即生效，不必重启电脑。请新开一个 PowerShell 窗口，再运行脚本。

The switch sets the execution policy to `RemoteSigned` for the **current user**. After that, scripts written or copied on this computer can run. Scripts downloaded from a browser, email, or a chat app still need a trusted digital signature, or they must be unblocked as described in the next section. The change takes effect at once. A restart is not required. Open a new PowerShell window before you run the script.

Windows 11：

1. 按 `Win + I` 打开**设置**。
2. 进入 **系统 → 开发者选项**。部分版本把这一页放在 **隐私和安全性 → 开发者选项**。
3. 展开 **PowerShell**。
4. 打开 “Change execution policy to allow local PowerShell scripts to run without signing. Require signing for remote scripts.”

On Windows 11:

1. Press `Win + I` to open **Settings**.
2. Go to **System → For developers**. On some builds this page is under **Privacy & security → For developers**.
3. Expand **PowerShell**.
4. Turn on “Change execution policy to allow local PowerShell scripts to run without signing. Require signing for remote scripts.”

Windows 10：

1. 打开**设置 → 更新和安全 → 开发者选项**。
2. 在 PowerShell 一项勾选上面同一句话。
3. 点击**应用**。

On Windows 10:

1. Open **Settings → Update & Security → For developers**.
2. Under PowerShell, check the same sentence.
3. Click **Apply**.

可以用下面的命令确认当前策略。期望结果是 `RemoteSigned`。

Confirm the policy with the command below. The expected result is `RemoteSigned`.

```powershell
Get-ExecutionPolicy
```

## 用一条命令完成同一项设置

## Make the same change from PowerShell

不方便进设置页面时，在普通 PowerShell 窗口（不必“以管理员身份运行”）执行：

When the Settings page is inconvenient, run this in a normal PowerShell window. “Run as administrator” is not required.

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

`CurrentUser` 只影响当前登录的账户，写入注册表后会一直保留，直到再次修改。PowerShell 会询问是否更改执行策略，输入 `Y` 确认。确认后再执行：

`CurrentUser` affects only the signed-in account. The value is stored in the registry and stays until someone changes it again. PowerShell asks for confirmation. Type `Y`. Then run:

```powershell
Set-Location -LiteralPath $PSScriptRoot
.\Windows.ps1
```

若你是从别的目录启动，把上面的 `Set-Location` 换成脚本所在文件夹，或直接写完整路径。

If you start from another directory, point `Set-Location` at the folder that contains the script, or pass the full path.

## 只放行这一次运行

## Allow this one run only

若客户不希望改动系统里长期有效的策略，可以从 `cmd` 或 PowerShell 用进程级放行启动。`Bypass` 只存在于这一次 PowerShell 进程，窗口关闭后即消失。

If a customer prefers not to change the lasting policy, start the script with a process-only exception from `cmd` or PowerShell. `Bypass` exists only for that PowerShell process and disappears when the window closes.

在脚本所在目录打开终端后执行：

From a terminal opened in the script folder:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\Windows.ps1
```

直接双击 `.ps1` 往往不会执行脚本。Windows 把这类文件的默认打开方式设为记事本，这是系统的安全默认行为。请用上面的命令，或在文件上右键选择“使用 PowerShell 运行”。右键运行仍然服从执行策略，因此在策略仍为 `Restricted` 时，需要先完成上一节的设置，或改用带 `-ExecutionPolicy Bypass` 的命令。

Double-clicking a `.ps1` file usually does not execute it. Windows associates these files with Notepad by default. That is a security default. Use the command above, or right-click the file and choose “Run with PowerShell”. The right-click action still obeys the execution policy, so while the policy remains `Restricted` you either complete the setting above or use the command that passes `-ExecutionPolicy Bypass`.

## 脚本来自下载时，再解除锁定

## Unblock the file when it was downloaded

策略已经是 `RemoteSigned`，但脚本仍无法启动时，先看它是不是从网页、邮件或压缩包里拿到的。Windows 会给这类文件加上来源标记（Mark of the Web）。`RemoteSigned` 把带标记的文件视为远程脚本，未签名就不能运行。

If the policy is already `RemoteSigned` and the script still will not start, check whether it arrived from a web page, an email message, or a zip archive. Windows attaches a Mark of the Web to those files. `RemoteSigned` treats a marked file as a remote script, and an unsigned remote script is blocked.

图形界面：右键 `Windows.ps1` → **属性** → **常规**。若底部有“解除锁定 / Unblock”，勾选后确定。

In File Explorer: right-click `Windows.ps1`, open **Properties**, then **General**. If **Unblock** appears at the bottom, check it and confirm.

命令行：

From PowerShell:

```powershell
Unblock-File -LiteralPath .\Windows.ps1
```

本机自己创建、且没有经过下载的副本不带这个标记，一般不需要这一步。

A copy created on this computer, and never downloaded, has no such mark and usually does not need this step.

## 设置无效时

## When the setting does not stay

公司电脑上，组策略“启用脚本执行 / Turn on Script Execution”的优先级高于“开发者选项”里的开关，也高于 `CurrentUser` 那条命令。策略被定为仅允许签名脚本，或被禁用时，设置开关会看起来点了却不起作用。这种情况需要管理员调整组策略，个人账户无法在本地覆盖。

On a managed PC, the Group Policy setting “Turn on Script Execution” outranks both the For developers switch and the `CurrentUser` command. When that policy allows only signed scripts, or disables scripts, the Settings switch can appear to turn on and still have no effect. An administrator has to change Group Policy. A personal account cannot override it locally.

可用下面的命令查看是哪一层把策略固定住了。`MachinePolicy` 或 `UserPolicy` 有具体值时，就是组策略在生效。

This command shows which scope is holding the policy. A value under `MachinePolicy` or `UserPolicy` means Group Policy is in effect.

```powershell
Get-ExecutionPolicy -List
```

## 脚本能够启动之后

## After the script is allowed to start

执行策略只解决“脚本能不能被 PowerShell 读入并运行”。脚本运行后还有两个使用上的说明：

The execution policy only decides whether PowerShell will load and run the file. After the script runs, two usage notes still apply.

- 本机已经有 npm 时，脚本打印版本后直接结束，不会重复安装 Node.js。
- When npm is already present, the script prints the version and exits. It does not install Node.js again.
- 本机没有 npm 时，安装由 winget 完成。winget 随 Microsoft Store 中的“应用安装程序 / App Installer”提供。若提示找不到 `winget`，先在 Microsoft Store 中安装或更新“应用安装程序”，再重新运行 `Windows.ps1`。
- When npm is missing, installation is done by winget. winget ships with **App Installer** from the Microsoft Store. If the terminal says `winget` cannot be found, install or update App Installer from the Store, then run `Windows.ps1` again.
- winget 把 Node.js 写进系统的 PATH。正在运行的这个窗口不会自动看到新的 `npm`。请关闭它，新开一个 PowerShell，再执行 `npm --version`。能打印出版本号，就表示这一步已经完成。
- winget adds Node.js to the system PATH. The window that is already open does not see the new `npm`. Close it, open a new PowerShell window, and run `npm --version`. A printed version number means this step is complete.
