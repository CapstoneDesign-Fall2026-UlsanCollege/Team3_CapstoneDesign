# Independent two-latte checkout verification

**Status:** Pending. A teammate who did not author the regression should execute and record this check.

1. Use an authorized demo café workspace with simulated payments, either on a local run or on the team’s Render candidate. Record `git rev-parse HEAD` for local or the commit shown for the active deploy in Render. If you cannot obtain the deployed SHA, record that limitation. Use a workspace where no one else will change inventory during the check.
2. Sign in, select the café workspace, and check the menu and recipe. One **Caffè Latte** must cost **KRW 4,500** and consume **250 ml Milk** and **18 g Coffee beans**. Confirm you have at least **500 ml** milk and **36 g** beans. Record their starting stock and units. Fresh seed values are 5,000 ml and 1,200 g.
3. Open browser DevTools → Network and keep it open. In Checkout, add exactly two lattes, select **Takeaway**, and save with **Create order**. Record the order ID from `POST /orders`. Confirm status `open`, quantity `2`, unit price `4500`, total `9000`, and unchanged stock.
4. Pay that order with simulated **Cash**. Record HTTP `200` from `POST /orders/{id}/pay`. Check the receipt showing two lattes and **KRW 9,000**, and record `payment_method`, `simulated_reference`, and `paid_at` from the response. Open Inventory or read `GET /inventory` and record both quantities. Expect milk −500 ml and coffee beans −36 g (4,500 ml and 1,164 g from the fresh seed).
5. If you have test database access, capture the ledger using the queries below before retrying. In the same signed-in tab, run the snippet with the order ID from step 3 and the API origin shown in Network. It reads the order and inventory, sends one **card** payment to the already-paid order, then reads both again. Expect retry HTTP `409` with “already been processed,” the original receipt and reference, and exactly the same stock. The `stockAfterRetry` values should agree with your step 4 records. If you captured the ledger, rerun the queries for comparison.

```javascript
{
  const api = location.origin; // Local Vite development uses "http://localhost:8000".
  const id = 123; // Replace with your order ID.
  const order = `/orders/${id}`;
  const read = async (path, options = {}) => {
    const response = await fetch(`${api}${path}`, {
      credentials: "include", cache: "no-store", ...options,
    });
    return { status: response.status, body: await response.json() };
  };
  const checked = async (path) => {
    const response = await read(path);
    if (response.status !== 200) throw new Error(`${path} returned HTTP ${response.status}`);
    return response.body;
  };
  const session = await checked("/auth/session");
  if (!session.authenticated || !session.store_id || !session.csrf_token) {
    throw new Error("Sign in and select the test café workspace first");
  }
  const receiptBefore = await checked(order);
  if (receiptBefore.id !== id || receiptBefore.status !== "paid" ||
      receiptBefore.total !== 9000 || receiptBefore.payment_method !== "cash" ||
      receiptBefore.items.length !== 1 || receiptBefore.items[0].name !== "Caffè Latte" ||
      receiptBefore.items[0].quantity !== 2 || !receiptBefore.simulated_reference) {
    throw new Error("Use the ID of the two-latte order you just paid in cash");
  }
  const stock = async () => (await checked("/inventory")).filter(
    (item) => ["Milk", "Coffee beans"].includes(item.name),
  );
  const stockBeforeRetry = await stock();
  const retry = await read(`${order}/pay`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "X-CSRF-Token": session.csrf_token },
    body: JSON.stringify({ method: "card" }),
  });
  const receiptAfter = await checked(order);
  const stockAfterRetry = await stock();
  console.log({ retry, receiptBefore, receiptAfter, stockBeforeRetry, stockAfterRetry });
}
```

The API exposes one receipt and current stock. To independently verify exact ledger rows, run the following read-only queries against the **test workspace’s database** after the cash payment and again after the card retry. Use the selected café’s `store_….db` for local SQLite or select the café’s schema on a local PostgreSQL instance. Replace `123` with the recorded order ID. Expect the same one `cash` payment for `9000` and the same two `paid_order` movements (Milk `−500`, Coffee beans `−36`) in both snapshots. If you only have browser access, record that the receipt and stock were checked through the API and leave ledger counts unverified for your run.

```sql
SELECT id, order_id, method, amount, simulated_reference, created_at
FROM payments WHERE order_id = 123 ORDER BY id;

SELECT m.id, m.order_id, i.name, i.unit, m.quantity_change, m.reason, m.created_at
FROM inventory_movements AS m JOIN ingredients AS i ON i.id = m.ingredient_id
WHERE m.order_id = 123 ORDER BY m.id;
```

Post your own result in [Issue #22](https://github.com/CapstoneDesign-Fall2026-UlsanCollege/Team3_CapstoneDesign/issues/22). Include your GitHub login, KST timestamp, environment, SHA, workspace, order ID, expected and actual total and stock deltas, first and retry HTTP status, reference before/after, and evidence links. Attach the receipt, stock and retry output, and ledger snapshots if available. Exclude cookies, CSRF tokens, and login details. If access or data prevents a check, record the blocker and the last completed step.

For an automated local rerun, install `requirements-dev.txt` from `smartserve-pos/backend`, then run `python -B -m unittest -v test_week12_ualsom` and `python -B -m unittest discover -v` in that directory. The automated test uses its own temporary SQLite database. [Test source](../../smartserve-pos/backend/test_week12_ualsom.py)
