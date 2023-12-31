const GET_ONE_ITEM = "/get-one-item";
const GET_ALL_ITEMS = "/get-all-items";
const DELETE_ITEM = "/delete-item";
const DELETE_USER_ITEMS = "/delete-user_items"

// action creators
const actionGetOneItem = (item) => ({
   type: GET_ONE_ITEM,
   item,
});

const actionGetAllItems = (items) => ({
   type: GET_ALL_ITEMS,
   items,
});

const actionDeleteItem = (itemId) => ({ type: DELETE_ITEM, itemId });

const actionDeleteUserItems = (userId) => ({type: DELETE_USER_ITEMS, userId})


// thunks

export const thunkCreateItem = (itemId) => async (dispatch) => {
   const res = await fetch(`/api/items/${itemId}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(itemId),
   });

   if (res.ok) {
      const data = await res.json();
      dispatch(actionGetOneItem(data));
      return data;
   } else {
      const errors = await res.json();
      return errors;
   }
};

export const thunkGetOneItem = (itemId) => async (dispatch) => {
   const res = await fetch(`/api/items/${itemId}`);

   if (res.ok) {
      const data = await res.json();
      dispatch(actionGetOneItem(data));
      return data;
   } else {
      const errors = await res.json();
      return errors;
   }
};

export const thunkGetAllItems = () => async (dispatch) => {
   const res = await fetch("/api/items");

   if (res.ok) {
      const data = await res.json();
      dispatch(actionGetAllItems(data));
      return data;
   } else {
      const errors = await res.json();
      return errors;
   }
};

export const thunkDeleteItem = (itemId) => async (dispatch) => {
   const res = await fetch(`/api/items/delete/${itemId}`, {
      method: "DELETE",
   });

   if (res.ok) {
      const data = await res.json();
      dispatch(actionDeleteItem(itemId));
      return data;
   } else {
      const errors = await res.json();
      return errors;
   }
};

export const thunkDeleteUserItems = (userId) => async (dispatch) => {
   const res = await fetch(`/api/items/user/${userId}/delete`, {
      method: "DELETE",
   });

   if (res.ok) {
      const data = await res.json();
      dispatch(actionDeleteUserItems(userId));
      return data;
   } else {
      const errors = await res.json();
      return errors;
   }
};

// reducer

const initialState = { allItems: {} };

export default function itemsReducer(state = initialState, action) {
   let newState;

   switch (action.type) {
      case GET_ONE_ITEM:
         newState = { ...state, allItems: { ...state.allItems } };
         newState.allItems[action.item.id] = action.item;
         return newState;

      case GET_ALL_ITEMS:
         newState = { ...state, allItems: {} };
         action.items.forEach(
            (item) => (newState.allItems[item.id] = item)
         );
         return newState;

      case DELETE_ITEM:
         newState = { ...state, allItems: { ...state.allItems } };
         delete newState.allItems[action.itemId];
         return newState;

      case DELETE_USER_ITEMS:
         return {...state, allItems: {}}

      default:
         return state;
   }
}
