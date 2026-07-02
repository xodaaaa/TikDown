import { useState } from "react";
import UsersTable from "./UsersTable";
import AddUserModal from "./AddUserModal";

export default function UsersPage() {
  const [showAdd, setShowAdd] = useState(false);

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold">Users</h1>
        <button
          onClick={() => setShowAdd(true)}
          className="px-4 py-2 bg-accent-600 hover:bg-accent-500 text-white rounded-lg text-sm font-medium transition-colors"
        >
          + Add User
        </button>
      </div>
      <UsersTable />
      {showAdd && <AddUserModal onClose={() => setShowAdd(false)} />}
    </div>
  );
}
