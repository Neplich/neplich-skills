type SettingsShellProps = {
  title: string;
  children: React.ReactNode;
};

export function SettingsShell({ title, children }: SettingsShellProps) {
  return (
    <div>
      <header>{title}</header>
      <main>{children}</main>
    </div>
  );
}
